# coding: utf-8
import os
import git
import datetime
import json
from Gitpard.apps.analysis import helpers
from django.http import Http404
from django.utils.safestring import mark_safe
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, detail_route
from Gitpard.apps.repository.models import Repository
from Gitpard.apps.analysis.models import Report
from rest_framework import status
from tasks import report
import serializers


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReportSerializer
    queryset = Report.objects

    @detail_route(methods=["post"])
    def delete(self, request, repo_id, pk):
        obj = Report.objects.get(pk=pk)
        if obj.state == Report.PREPARED:
            return Response({
                "error": {
                    "code": -1,
                    "message": "Access Denied",
                    "description": u"Отчёт подготавливается. Удаление невозможно."
                }})
        else:
            # TODO удалить файл отчёта если такой есть
            obj.delete()
            return Response({
                "code": 1,
                "message": "Success",
                "description": u"Отчёт успешно удалён"
            })

    def create(self, request, *args, **kwargs):
        # Переопределил метод чтобы воткнуть в контекст сериализатора объект репозитория
        # Так же здесь преобразовываю маску из JSON в str, т.к. SQLite не может хранить JSON,
        # а встроенный валидатор искажает данные
        # TODO если будет найдено менее костыльное решение, заменить

        # begin
        data = request.data
        if not isinstance(request.data['mask'], dict):
            raise ValidationError(u"Bad request. Mask must be JSON")
        data['mask'] = json.dumps(request.data['mask'])
        repo_obj = get_object_or_404(Repository, pk=self.kwargs['repo_id'], user=request.user)
        if not repo_obj.state == Repository.LOADED:
            raise ValidationError(u"Репозиторий заблокирован. Невозможно создать отчёт.")
        serializer = self.get_serializer(data=data)
        serializer.context["repository"] = repo_obj
        repo_obj.mask = data['mask']
        repo_obj.save(update_fields=['mask'])
        # end

        # copy-paste from super method
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        report.delay(serializer.data['id'])  # start task
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        # Блокировка супер-метода удаления
        raise NotImplementedError

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_dict = serializer.data
        response_dict["repo_name"] = instance.repository.name
        try:
            response_dict["mask"] = json.loads(serializer.data["mask"]) if serializer.data["mask"] else {"include": [],
                                                                                                         "exclude": []}
        except ValueError:
            response_dict["mask"] = {"include": [], "exclude": []}
        try:
            response_dict["report"] = json.loads(serializer.data["report"]) if serializer.data["report"] else []
        except ValueError:
            response_dict["report"] = []
        return Response(response_dict)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        repo_obj = get_object_or_404(Repository, pk=self.kwargs['repo_id'], user=request.user)
        if not repo_obj.state == Repository.LOADED:
            return Response(
                {'error':
                     {"code": -1,
                      "message": "Repository locked",
                      "description": u"Репозиторий недоступен"}
                 }
            )
        try:
            repo = git.Repo(repo_obj.path)
            branches = [{"branch_name": r.name} for r in repo.heads]
            for data in serializer.data:
                del data['mask']
                del data['report']
            try:
                mask = json.loads(repo_obj.mask) if repo_obj.mask else {"include": [], "exclude": []}
            except ValueError:
                mask = {"include": [], "exclude": []}
            response_dict = {
                "branches": branches,
                "mask": mask,
                "reports": serializer.data
            }
        except git.GitCommandError:
            return Response(
                {'error':
                     {"code": -2,
                      "message": "Repository error",
                      "description": u"Ошибка при обработке репозитория"}
                 }
            )
        else:
            return Response(response_dict)

    def get_queryset(self):
        return Report.objects.filter(repository=self.kwargs['repo_id'])


@api_view(['GET'])
def branches(request, repo_id, *args, **kwargs):
    repo_obj = get_object_or_404(Repository, pk=repo_id, user=request.user)
    if not repo_obj.state == Repository.LOADED:
        return Response(
            {'error':
                 {"code": -1,
                  "message": "Repository locked",
                  "description": u"Репозиторий недоступен"}
             }
        )
    repo = git.Repo(repo_obj.path)
    branches = [{"branch_name": r.name} for r in repo.heads]
    return Response({"branches": branches})


@api_view(['GET'])
def branch_tree(request, repo_id, branch, *args, **kwargs):
    obj = get_object_or_404(Repository, pk=repo_id, user=request.user)
    if not obj.state == Repository.LOADED:
        return Response(
            {'error':
                 {"code": -1,
                  "message": "Repository locked",
                  "description": u"Репозиторий недоступен"}
             }
        )
    last = obj.state
    obj.state = Repository.BLOCKED
    obj.save(update_fields=['state'])
    print 'chmod'
    print  repo_id
    print  branch
    print  request.user
    # try:
    tree = helpers.get_tree(repo_id, branch, request.user)
    # except Exception:
    #     return Response(
    #         {'error':
    #              {"code": -2,
    #               "message": "Something wrong",
    #               "description": u"Что-то не так"}
    #          }
    #     )
    # finally:
    obj.state = last
    obj.save(update_fields=['state'])
    return Response(tree)


@api_view(['POST'])
def masked_branch_tree(request, repo_id, *args, **kwargs):
    data = request.data
    obj = get_object_or_404(Repository, pk=repo_id, user=request.user)
    if not obj.state == Repository.LOADED:
        return Response(
            {'error':
                 {"code": -1,
                  "message": "Repository locked",
                  "description": u"Репозиторий недоступен"}
             }
        )
    last = obj.state
    obj.state = Repository.BLOCKED
    obj.save(update_fields=['state'])
    try:
        files = helpers.get_files(repo_id, data['branch'], data['mask'])
        tree = helpers.get_tree(repo_id, data['branch'], request.user, mask=files)
    except ValueError as e:
        raise ValidationError(e.message)
    except:
        return Response(
            {'error':
                 {"code": -2,
                  "message": "Something wrong",
                  "description": u"Что-то не так"}
             }
        )
    finally:
        obj.state = last
        obj.save(update_fields=['state'])
    return Response(tree)


@api_view(['GET'])
def annotation_file(request, repo_id, branch, file_path, *args, **kwargs):
    """
    :param request:
    :param repo_id: int
    :param branch: string
    :param file_path: string
    :param args:
    :param kwargs:
    :return: json
    """
    repo_obj = get_object_or_404(Repository, pk=repo_id, user=request.user)
    if not repo_obj.state == Repository.LOADED:
        return Response(
            {'error':
                 {"code": -1,
                  "message": "Repository locked",
                  "description": u"Репозиторий недоступен"}
             }
        )
    last = repo_obj.state
    repo_obj.state = Repository.BLOCKED
    repo_obj.save(update_fields=['state'])
    repo = git.Repo(repo_obj.path)
    try:
        repo.git.checkout(branch)
        temp = []
        index = 1
        for commit, lines in repo.blame(branch, file_path):
            for line in lines:
                temp.append({
                    "number": index,
                    "line": unicode(line),
                    "author": commit.author.name,
                    "created_date": datetime.datetime.fromtimestamp(commit.authored_date),
                    "commit": commit.hexsha})
                index += 1
        return Response({'data': temp})
    except git.GitCommandError:
        return Response(
            {'error':
                 {"code": -2,
                  "message": "Bad request",
                  "description": u"Файл не найден"}
             }
        )
    except UnicodeDecodeError:
        return Response(
            {'error':
                 {"code": -3,
                  "message": "Bad file",
                  "description": u"Невозможно прочитать файл"}
             }
        )
    finally:
        repo_obj.state = last
        repo_obj.save(update_fields=['state'])
