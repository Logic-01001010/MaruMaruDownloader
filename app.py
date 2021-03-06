import requests
from bs4 import BeautifulSoup
import os
import time


base_url = None

# 정규 표현 필터 함수
def Reg(name):

	import re

	a = re.compile('[(]\d[)][개]') # 댓글 유무
	result = a.search( name )

	if( result ):
		return name.replace( result[0], '' )

	else:
		return name


def filter_name(name):

	name = name.replace('\t\t\t\t', ' ')
	name = name.replace('\t\t\t', ' ')
	name = name.replace('\t\t', ' ')
	name = name.replace('\t', ' ')
	name = name.replace('\\', '~')
	name = name.replace('/', '~')
	name = name.replace(':', '~')
	name = name.replace('*', '~')
	name = name.replace('?', '~')
	name = name.replace('"', '~')
	name = name.replace('<', '~')
	name = name.replace('>', '~')
	name = name.replace('|', '~')

	name = Reg( name ).strip()

	result = name

	return result



def createFolder(name):

	if not os.path.exists(name):
		os.makedirs(name)


def saveImage( url, name ):

	res = requests.get(url)
	file = open(name, "wb")
	file.write( res.content )
	file.close()



def saveManga( title, link ):

	global base_url

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

			# Canvas일 경우에
			if base_url not in img_url:
				img_url = base_url + img_url


			print( '(' + str(cur) + '/'  + str(list_size) + ')' + ' : ' + img_url ) # 현재 진행도
	
			
			saveImage( img_url, title + '/'+ str(count) + ext) # title은 디렉토리 이름

			cur += 1
			count += 1
	else:
		print( res.status_code )



if __name__ == '__main__':

	url = input('다운 받고자 하는 만화 URL 입력: ')
	save_folder = input('저장될 폴더의 이름 입력: ')
	createFolder( save_folder )

	base_url = url.rsplit('/', 3)[0]

	start_time = time.time()


	res = requests.get(url)

	if res.status_code == 200:
		html = res.text
		soup = BeautifulSoup(html, 'html.parser')


		tables = soup.select( 'table.table.div-table.list-pc.bg-white .list-subject a' )


		list_size = len( tables )
		cur = 1

		# 테이블 제목 추출
		for table in tables:

			title = filter_name( (table.get_text().strip()) )

			link = table.attrs['href']
			print("====================================================")
			print( '(' + str(cur) + '/'  + str(list_size) + ')' ) # 현재 진행도
			print( '제목: ' + title )
			print( 'URL: ' + base_url + link )
			print("====================================================")

			# 폴더 생성
			createFolder( save_folder +'/'+ title )

			# 만화 저장
			saveManga( save_folder +'/'+ title, base_url + link )

			cur += 1


		print('\n****************************')
		print('\a작업 완료. 총 ' + str(round(time.time() - start_time, 1)) + '초 소요.')
		print('****************************\n')


	else:
		print( res.status_code )