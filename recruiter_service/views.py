from job_easy.models import job, application,User,employer_profile,employee_profile,credibility
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import recruiter_Serializer


def CountFrequency(my_list):
    freq = {}
    for item in my_list:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1
    for k,v in freq.items():
        freq[k]=v/len(my_list)
    return freq


class recruiter_website(APIView):

    def get(self,request):
        params={}

        all_apps=[]
        for each in application.objects.filter(application_status="Selected"):
            all_apps.append((each.job.job_type,each.user.email))

        all_apps_dict_job_wise={}
        for each in all_apps:
            try:
                all_apps_dict_job_wise[each[0]].append(each[1])
            except:
                all_apps_dict_job_wise[each[0]]=[each[1]]

        print(all_apps_dict_job_wise)

        final_all_apps_dict_job_wise={}
        for eachk,eachv in all_apps_dict_job_wise.items():
            final_all_apps_dict_job_wise[eachk]=CountFrequency(eachv)

        params["best_applicants"]=final_all_apps_dict_job_wise

        employer_by_ratings=credibility.objects.order_by('-ratings')

        employer_by_ratings_dict={}
        for each in employer_by_ratings:
            try:
                employer_by_ratings_dict[each.on_user.job.user].append(each.ratings)
            except:
                employer_by_ratings_dict[each.on_user.job.user]=[each.ratings]

        average_rating_for_each_user={}
        for k,v in employer_by_ratings_dict.items():
            sum1=0
            for each in v:
                sum1+=int(each)
            average_rating_for_each_user[k]=sum1/len(v)

        params["best_recruiters"]=[]
        for k,v in average_rating_for_each_user.items():
            params["best_recruiters"].append({User.objects.get(username=k).email:[v,User.objects.get(username=k).username]})

        params=[params]

        serializer = recruiter_Serializer(data={'input_values': params})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return Response(data)