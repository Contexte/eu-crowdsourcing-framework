@blueprint.route('/<short_name>/tasks/analyze')
def analyze(short_name):
    (project, owner, n_tasks, n_task_runs,
    overall_progress, last_activity) = project_by_shortname(short_name)
   
    def gen_json(table):
        n = getattr(task_repo, 'count_%ss_with' % table)(project_id=project.id)
        sep = ", "
        json_string = "["
        for i, tr in enumerate(getattr(task_repo, 'filter_%ss_by' % table)(project_id=project.id), 1):
            item = json.dumps(tr.dictize())
            if (i == n):
                sep = ""
            json_string += (item + sep)
        json_string += "]"
        return json_string

    json_pybossa_project_datas = gen_json("task_run")

    return render_template('/projects/analyzer.html', json_pybossa_project_datas = json_pybossa_project_datas)
