# -*- coding: utf-8 -*-
import shutil

from datetime import datetime

import os
import git
from Gitpard.apps.repository.models import Repository
import json
from Gitpard.apps.analysis.helpers import get_files
from celery.task import task
from Gitpard.apps.analysis.models import Report
import django
django.setup()


@task(ignore_result=True)
def report(obj_id):
    try:
        report_obj = Report.objects.get(pk=obj_id)
        repo_id = report_obj.repository.id
        repo_obj = Repository.objects.get(pk=repo_id)
        branch = report_obj.branch
        mask = json.loads(report_obj.mask)
        if repo_obj.state != Repository.LOADED:
            report_obj.state = Report.FAILED
            report_obj.save(update_fields=["state"])
            return
        repo_obj.state = Repository.BLOCKED
        repo_obj.save(update_fields=['state'])
        repo = git.Repo(repo_obj.path)
        files = get_files(repo_id, branch, mask)
        repo.git.checkout(branch)
        stat = {}
        for f in files:
            file_path = os.path.join(repo_obj.path, f)
            stat[f] = []
            try:
                for commit, lines in repo.blame(branch, file_path):
                    for line in lines:
                        line = unicode(line)
                        if line.strip():
                            stat[f].append({
                                "author": commit.author.name,
                                "delta": (datetime.now() - datetime.fromtimestamp(commit.authored_date)).total_seconds()
                            })
            except UnicodeDecodeError:
                if f in stat:
                    del stat[f]
                continue
        if report_obj.kind == Report.ON_AUTORS:
            authors_stat = {}
            for key, value in stat.iteritems():
                for line in value:
                    if not line["author"] in authors_stat:
                        authors_stat[line["author"]] = {
                            "total_time": 0,
                            "total_lines": 0
                        }
                    else:
                        authors_stat[line["author"]]["total_time"] += line["delta"]
                        authors_stat[line["author"]]["total_lines"] += 1
            result = []
            for key, value in authors_stat.iteritems():
                if value["total_lines"]:
                    result.append({
                        "key": key,
                        "result": (value["total_time"]/value["total_lines"]) / 86400
                    })
                else:
                    result.append({
                        "key": key,
                        "result": 0
                    })
            report_obj.report = json.dumps(result)
            report_obj.save(update_fields=["report"])
        elif report_obj.kind == Report.ON_FILES:
            result = []
            for key, value in stat.iteritems():
                file_name = key
                total_lines = len(value)
                total_time = 0
                if total_lines:
                    for line in value:
                        total_time += line["delta"]
                    result.append({
                        "key": file_name,
                        "result": (total_time/total_lines) / 86400
                    })
                else:
                    result.append({
                        "key": file_name,
                        "result": 0
                    })
            report_obj.report = json.dumps(result)
            report_obj.save(update_fields=["report"])
    except Report.DoesNotExist:
        print "Initialization failed. No such report object."
    except git.GitCommandError as ge:
        print "Git error: ", str(ge)
        report_obj.state = -1
        report_obj.save(update_fields=['state'])
    else:
        report_obj.state = 1
        report_obj.save(update_fields=['state'])
    finally:
        repo_obj.state = Repository.LOADED
        repo_obj.save(update_fields=['state'])
