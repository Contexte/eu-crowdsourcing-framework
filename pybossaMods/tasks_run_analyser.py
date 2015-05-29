#/usr/bin/ptyhon
import json
import re
from pprint import pprint
from collections import defaultdict

eu_consultation_project_datas_dict = {}

print "Enter the path to the file :"
json_file_to_treat = raw_input()

with open(json_file_to_treat) as data_file:
	json_untreated_data_from_pybossa = json.load(data_file)

for task_run in json_untreated_data_from_pybossa:
	for infos in task_run["info"]:
		task_run_infos = infos["name"]
		response = infos["value"]
		regexp_match_on_task_run = re.match(r'(.*)!!(.*)!!(.*)!!', 
							task_run_infos)

		organization = regexp_match_on_task_run.group(1)
		child_pdf = regexp_match_on_task_run.group(2)
		question = regexp_match_on_task_run.group(3)

                eu_consultation_project_datas_dict.\
                                setdefault(organization, {child_pdf : {question : []}})
		eu_consultation_project_datas_dict\
                                [organization]\
                                .setdefault(child_pdf, {question : []})
		eu_consultation_project_datas_dict\
                                [organization]\
                                [child_pdf]\
                                .setdefault(question, [])
		eu_consultation_project_datas_dict\
				[organization]\
				[child_pdf]\
				[question]\
				.append(response)
		

# This is just a test, to display datas on the console.
for ppdf in eu_consultation_project_datas_dict:
	print ppdf
	for cpdf in eu_consultation_project_datas_dict[ppdf]:
		print 	"	", cpdf
		for q in eu_consultation_project_datas_dict[ppdf][cpdf]:
			print 	"		", q
			for a in eu_consultation_project_datas_dict[ppdf][cpdf][q]:
				print	"			", a
