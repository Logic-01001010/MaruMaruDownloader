import requests
from bs4 import BeautifulSoup
import os


def createFolder(name):

	if not os.path.exists(name):
		os.makedirs(name)


def saveImage( url, name ):

	res = requests.get(url)
	file = open(name, "wb")
	file.write( res.content )
	file.close()



def saveManga( title, link ):

	url = link

	res = requests.get(url)


	if res.status_code == 200:
		html = res.text
		soup = BeautifulSoup(html, 'html.parser')


		images = soup.select( '.view-img img' )


		list_size = len( images )
		cur = 1
		count = 1

		# 만화 이미지 추출
		for image in images:
			img_url = image.attrs['src']
			ext = '.'+img_url[-3:]

			print( '(' + str(cur) + '/'  + str(list_size) + ')' + ' : ' + img_url ) # 현재 진행도
	
			
			saveImage( img_url, title + '\\'+ str(count) + ext) # title은 디렉토리 이름

			cur += 1
			count += 1
	else:
		print( res.status_code )



if __name__ == '__main__':


	url = input('다운 받고자 하는 만화 URL 입력: ')


	res = requests.get(url)

	if res.status_code == 200:
		html = res.text
		soup = BeautifulSoup(html, 'html.parser')


		tables = soup.select( 'table.table.div-table.list-pc.bg-white .list-subject a' )


		list_size = len( tables )
		cur = 1

		# 테이블 제목 추출
		for table in tables:

			title = table.get_text().strip()
			link = table.attrs['href']
			print("====================")
			print( '(' + str(cur) + '/'  + str(list_size) + ')' ) # 현재 진행도
			print( '제목: ' + title )
			print( 'URL: ' + 'https://marumaru.cloud'+link )
			print("====================")

			# 폴더 생성
			createFolder( title )

			# 만화 저장
			saveManga( title, 'https://marumaru.cloud'+link )

			cur += 1


	else:
		print( res.status_code )