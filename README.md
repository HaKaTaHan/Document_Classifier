# Document_Classifier
인공지능을 이용한 문서 분류

## 개요
반복적으로 분류할 필요가 있는 문서의 표지를 학습시킨 모델을 기반으로 문서를 표지와 내용으로 분류하고, 표지 단위로 문서를 나누어 저장합니다.
또한 표지의 제목에 해당하는 문자열을 OCR로 읽어 원하는 문서들을 따로 분류할 수 있습니다.

## 주요 기능
1. PDF 문서 묶음을 장 단위로 분리하여 IMG/IMG 폴더에 jpg 파일로 저장합니다.
> <img width="500" alt="PDFtoIMG" src="https://user-images.githubusercontent.com/37128456/79857263-796cce00-8408-11ea-9b4d-8f9d9235ae63.png">

2. 스캔 등으로 인하여 기울어진 이미지를 보정합니다.
> <img width="500" alt="degree" src="https://user-images.githubusercontent.com/37128456/79857747-38c18480-8409-11ea-8d3f-a1e05e540814.png">

3. 보정이 끝난 이미지들을 모델을 통해 분류하고, 사용자에게 보여줍니다. 이 때 사용자는 올바르게 분류되지 않은 이미지를 클릭하여 분류를 바꿀 수 있습니다(이미지는 블러처리 하였습니다).
##### 표지로 분류된 이미지들
> <img width="500" alt="Cover" src="https://user-images.githubusercontent.com/37128456/79859283-ba1a1680-840b-11ea-805b-4049c442f6ee.png">

##### 내용으로 분류된 이미지들(오차가 작은 상위 10개의 이미지만 표시합니다)
> <img width="500" alt="Content" src="https://user-images.githubusercontent.com/37128456/79858931-26e0e100-840b-11ea-8fae-a11789b78145.png">

4. 문자열 탐색을 실행할 것인지 묻습니다. 아니오를 클릭할 시 표지 단위로 문서를 분리하여 저장하고 6번으로 넘어갑니다.
> <img width="500" alt="ask" src="https://user-images.githubusercontent.com/37128456/79860910-7bd22680-840e-11ea-8d2e-edc9c36e8f91.png">

5-1. 예를 클릭할 시 탐색할 문자열을 입력 받습니다.
> <img width="500" alt="keyword" src="https://user-images.githubusercontent.com/37128456/79861018-a4f2b700-840e-11ea-9f3e-6398d1512943.png">

5-2. 표지 이미지에 대해 제목 부분을 자르고, OCR로 읽기 쉽게 보정한 후 문자열을 읽습니다.
> <img width="500" alt="ocr" src="https://user-images.githubusercontent.com/37128456/79861191-f56a1480-840e-11ea-913c-125d95b52e6b.png">

6. Result 폴더에 분류된 결과대로 폴더를 생성하고 프로그램을 종료합니다.
> <img width="500" alt="ocr" src="https://user-images.githubusercontent.com/37128456/79861315-32360b80-840f-11ea-9d4f-c32c845799e5.png">

## 실행 결과
폴더에 분류하여 저장됩니다.
> <img width="500" alt="ocr" src="https://user-images.githubusercontent.com/37128456/79862609-51359d00-8411-11ea-99a3-640ea6eb38a1.png">

## 사용 환경
* Python 3.6 이상
* Click 7.0
* Jinja2 2.11.1
* Pillow 7.0.0
* PyPDF2 1.26.0
* PyQt5 5.14.1
* PyQt5-sip 12.7.0
* PyQt5-stubs 5.13.1.4
* PyYAML 5.3
* attrs 18.2.0
* certifi 2019.11.28
* cffi 1.13.2
* chardet 3.0.4
* colorama 0.3.9
* cryptography 2.8
* cursor 1.3.4
* docx2pdf 0.1.5
* halo 0.0.28
* idna 2.8
* improtlib-metadata 1.5.0
* joblib 0.14.1
* log-symbols 0.0.14
* lxml 4.5.0
* marshmallow 2.20.5
* numpy 1.18.1
* opencv-python 4.1.2.30
* pdf2image 1.11.0
* pip 19.0.3
* progressbar2 3.47.0
* prompt-toolkit 2.0.10
* pyOpenSSL 19.1.0
* pycparser 2.19
* pyqt5-tools 5.13.0.1.5
* pytesseract 0.3.1
* python-docx 0.8.10
* python-dotenv 0.10.5
* python-utils 2.3.0
* pywin32 227
* requests 2.22.0
* requests-toolbelt 0.9.1
* scikit-learn 0.21.2
* scipy 1.4.1
* setuptools 40.8.0
* shellingham 1.3.1
* six 1.14.0
* spinners 0.0.23
* termcolor 1.1.0
* terminaltables 3.1.0
* torch 1.4.0
* torchvision 0.5.0
* tqdm 4.43.0
* urllib3 1.25.8
* wcwidth 0.1.8
* zipp 3.0.0

## 실행 전 설정
* 프로젝트 폴더에 CROP, IMG, Improvement, PDF, RePDF, Result 라는 이름의 폴더를 생성합니다.
> <img width="100" alt="folder_list" src="https://user-images.githubusercontent.com/37128456/79854198-0f522a00-8404-11ea-8c40-bf5ca8437045.png">

* IMG 폴더 내에 다시 IMG 폴더를 생성합니다.
> <img width="300" alt="IMG_in_IMG" src="https://user-images.githubusercontent.com/37128456/79854555-93a4ad00-8404-11ea-9b9a-14c1fb39da42.png">

* 분류를 원하는 PDF 파일(들)을 PDF 폴더 내에 넣습니다. 
> <img width="300" alt="PDF_located" src="https://user-images.githubusercontent.com/37128456/79853703-58ee4500-8403-11ea-9d2b-efda709286ba.png">

* 실행합니다.
> <img width="500" alt="RUN" src="https://user-images.githubusercontent.com/37128456/79853776-728f8c80-8403-11ea-9c16-a5ea34932e46.png">