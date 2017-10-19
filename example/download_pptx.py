from presentation import Present

def main():
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
	pptx = Present("../../key.json")
	buffer = pptx.create("Temp2", data=data)
	
	f = open('download.pptx', 'wb')
	f.write(buffer.getvalue())

if __name__ == '__main__':
	main()