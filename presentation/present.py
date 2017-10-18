import io
import time
import httplib2

from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from apiclient.http import MediaIoBaseDownload

class Present:
	__outputFolderName = "SlidesOutput"
	def __init__(self, filename):
		credentials = self.__get_credentials(filename)
		http = credentials.authorize(httplib2.Http())
		self.slides = discovery.build('slides', 'v1', http=http)
		self.drive = discovery.build('drive', 'v3', http=http)

	def __get_credentials(self, filename):
		scopes = (
			'https://www.googleapis.com/auth/presentations',
			'https://www.googleapis.com/auth/drive',
		)
		credentials = ServiceAccountCredentials.from_json_keyfile_name(filename, scopes)
		return credentials

	def __create_product_slide(self, index, data):
		pageId = "product_{0}".format(index)
		return [{
			"createSlide": {
				"objectId": pageId,
				"insertionIndex": 2 + index,
				"slideLayoutReference": {
					"predefinedLayout": "TITLE_AND_BODY"
				},
				"placeholderIdMappings": [
					{
						"layoutPlaceholder": {
							"type": "TITLE",
							"index": 0
						},
						"objectId": "{0}_title".format(pageId),
					},
					{
						"layoutPlaceholder": {
							"type": "BODY",
							"index": 0
						},
						"objectId": "{0}_body".format(pageId),
					},
				],
			}
		},
		{
			"insertText": {
				"objectId": "{0}_title".format(pageId),
				"text": data['product_name'],
			}
		},
		{
			"insertText": {
				"objectId": "{0}_body".format(pageId),
				"text": data['product_description'],
			}
		},
		{	
			"createImage": {
				"objectId": "{0}_img".format(pageId),
				"url": data["product_img"],
				"elementProperties": {
					"pageObjectId": pageId,
					"size": {
						"height": {
							"magnitude": 250,
							"unit": "PT",
						},
						"width":  {
							"magnitude": 250,
							"unit": "PT",
						}
					},
					"transform": {
						"scaleX": 1,
						"scaleY": 1,
						"translateX": 450,
						"translateY": 100,
						"unit": "PT"
					}
				}
			}
		},]

	def __create_default_slide(self, data, agenda):
		return [
		{
			'replaceAllText': {
				'containsText': {
					'text': '{{title}}',
					'matchCase': True
				},
				'replaceText': data['title']
			}
		},
		{
			'replaceAllText': {
				'containsText': {
					'text': '{{presentation_by}}',
					'matchCase': True
				},
				'replaceText': data['presentation_by']
			}
		},
		{
			'replaceAllText': {
				'containsText': {
					'text': '{{agenda}}',
					'matchCase': True
				},
				'replaceText': agenda
			}
		},
	]

	def __duplicate_slide(self, template):
		outputFolderId = self.drive.files().list(q="name='%s'" % self.__outputFolderName).execute().get('files')[0]['id']
		templateFileId = self.drive.files().list(q="name='%s'" % template).execute().get('files')[0]['id']

		body = {
			'name': '{0}-Slides'.format(time.strftime("%Y%m%d%H%M%S")),
			'parents' : [ outputFolderId ]
		}
		presentationId = self.drive.files().copy(fileId=templateFileId, body=body).execute().get('id')
		return presentationId

	def __fill_in_data(self, presentationId, data):
		agenda = "\n".join(list(map(lambda item:item['product_name'], data['product'])))
		requests = self.__create_default_slide(data['default'], agenda)

		for index, item in enumerate(data['product']):
			requests.append(self.__create_product_slide(index, item))

		body = {
			'requests': requests
		}
		response = self.slides.presentations().batchUpdate(presentationId=presentationId, body=body).execute()

	def __download_data(self, presentationId):
		request = self.drive.files().export_media(fileId=presentationId, mimeType="application/vnd.openxmlformats-officedocument.presentationml.presentation")
		fh = io.BytesIO()
		downloader = MediaIoBaseDownload(fh, request)
		done = False
		while done is False:
			status, done = downloader.next_chunk()
			print("Download %d%%" % int(status.progress() * 100))

		return fh

	def __delete_file(self, presentationId):
		self.drive.files().delete(fileId=presentationId).execute()

	def create(self, template, data):
		presentationId = self.__duplicate_slide(template)
		self.__fill_in_data(presentationId, data)
		file = self.__download_data(presentationId)
		self.__delete_file(presentationId)
		print(presentationId)
		return file
