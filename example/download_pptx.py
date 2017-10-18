import presentation
#from presentation import Present

def main():
	#pptx = Present("../../key.json")
	print("test")

'''
from django.shortcuts import render
from .present import Present
from django.http import HttpResponse
from django.conf import settings

# Create your views here.
def download(request):
	response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
	data={
		'default':{
			'title':'Product Intradtion',
			'presentation_by':'Charlie'
		},
		'product':[
			{'product_name':'product one', 'product_description':"This is Product one", 'product_img':'https://www.google.com.tw/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png'},
			{'product_name':'product two', 'product_description':"This is Product two", 'product_img':'https://lh3.googleusercontent.com/-REC9hG2lrlY/AAAAAAAAAAI/AAAAAAAANQ4/ZzlrQAV6pyE/photo.jpg'},
		]
	}
	pr = Present(settings.GOOGLE_KEY)
	buffer = pr.create(template="Temp2", data=data)

	file = buffer.getvalue()
	buffer.close()
	response.write(file)

	return response
'''

if __name__ == '__main__':
	#sys.path.append(os.path.dirname(sys.path[0]))
	main()