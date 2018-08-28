from django import forms
from .models import palypath

class AddForm(forms.Form):

	ip = forms.CharField()
	# playbook_path = forms.CharField()

	fun_list = (
		(1, 'zabbix_agent'),
		(2, '成都'),
		(3, '北京'),
	)
	fun_list=palypath.objects.all().values_list("id","func")
	playbook_path = forms.IntegerField(widget=forms.Select(choices=fun_list))
	# user_type_choice = (
	# 	(1, '普通用户'),
	# 	(2, '高级用户'),
	# )
	# book_type = forms.TypedChoiceField(coerce=lambda x: x=='1',widget=forms.CheckboxSelectMultiple(),choices=user_type_choice)
# def __init__(self, *args, **kwargs):
# 	#每次创建Form1对象时执行init方法
# 	super(AddForm, self).__init__(*args, **kwargs)
# 	user_type_choice = (
# 		(0, '普通用户'),
# 		(1, '高级用户'),
# 	)
# 	self.fields['book_type'] = forms.CharField(widget=forms.widgets.Select(choices=user_type_choice,attrs={'class': "form-control"}))