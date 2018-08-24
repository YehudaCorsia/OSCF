from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, CategoriesOptions
from watson_developer_cloud import NaturalLanguageUnderstandingV1, VisualRecognitionV3
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
import re, requests, random, sys, json

# Globals
MAX_IMAGES_CHECK_IN_WEBSITE = 5
DATABASE_NAME               = "sinun_db"


################### CREDENTIALS ######################
# Here is all the credentials that needed for working with all services.
# Enter yours credentials
# After you sign to services, you can get there credentials from here : "https://console.bluemix.net/dashboard/apps" 

# Cloudant credentials.
USERNAME_CLOUDANT = ""
PASSWORD_CLOUDANT = ""
URL_CLOUDANT      = ""

# NLU credentials.
USERNAME_NLU = ''
PASSWORD_NLU = ''
VERSION_NLU  = ''

# Visual Recognition credentials.
VERSION_VISUAL_RECOGNITION     = ''
URL_VISUAL_RECOGNITION         = ''
IAM_API_KEY_VISUAL_RECOGNITION =''

######################################################

#
#
# get_url_images_in_text()
#
# @param html - the html to extract urls of images from him.
# @param protocol - the protocol of the website, for append to urls that not start with protocol.
#
# @return list of imags url.
#
#
def get_url_images_in_text(html, protocol):
    urls = []
    all_urls = re.findall(r'((http\:|https\:)?\/\/[^"\' ]*?\.(png|jpg))', html, flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
    for url in all_urls:
        if not url[0].startswith("http"):
            urls.append(protocol + url[0])
        else:
            urls.append(url[0])

    return urls

#
#
# get_images_from_url()
#
# @param url - the url for extract images url from him. 
#
# @return list of images url.
#
#
def get_images_from_url(url):
    protocol = url.split('/')[0]
    resp = requests.get(url)
    return get_url_images_in_text(resp.text, protocol)

# Filtering with NLU (Natural language understanding).
# @return bool true if url was filtering, false  if not.
def filter_using_nlu(url):
    black_list_concepts = ["porn", "erotic", "sexolog"]
    black_list_keywords = ["porn", "ebony", "milf", "tits", "xxx", "anal", "gay"]
    
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version  = VERSION_NLU,
        username = USERNAME_NLU,
        password = PASSWORD_NLU
    )
    analysis = natural_language_understanding.analyze(
        url=url,
        features=Features(
            concepts=EntitiesOptions(
                emotion=True,
                sentiment=True),
            keywords=KeywordsOptions(
                emotion=True,
                sentiment=True)))
    
    for concept in analysis["concepts"]:
        for black_concept in black_list_concepts:
            if concept["text"].startswith(black_concept):
                print("The concept '" + concept["text"] + "' was found in url.")
                return False

    for keyword in analysis["keywords"]:
        for black_keyword in black_list_keywords:
            if keyword["text"].startswith(black_keyword):
                print("The keyword '" + keyword["text"] + "' was found in url.")
                return False
        return True

def filtering_with_visual_recognition(url):
    visual_recognition = VisualRecognitionV3(
        version = VERSION_VISUAL_RECOGNITION,
        url = URL_VISUAL_RECOGNITION,
        iam_api_key = IAM_API_KEY_VISUAL_RECOGNITION)
    
    images_links = get_images_from_url(url)
    
    # check random MAX_IMAGES_CHECK_IN_WEBSITE images in the url.
    for url in random.sample(images_links, k=min(MAX_IMAGES_CHECK_IN_WEBSITE, len(images_links))):
        classes = visual_recognition.classify(
                classifier_ids = ["explicit"],
                url = url
            )
        if classes["images"][0]["classifiers"][0]["classes"][0]["class"] != "not explicit":
            print("The image " + url + " was found explicit by visual recognistion.")
            return False
    return True

#
#
# main()
#
# @param url_to_check - dictionary object that contain the url.
#
# @return website_is_ok true if the url dosent contain problematic content false otherwise.
#
#
def main(url_to_check):
    # Use cloudant DB for save websites result.
    # Assumes that the database has been prepared in the past.
    client_cloudant = Cloudant(USERNAME_CLOUDANT, PASSWORD_CLOUDANT, url=URL_CLOUDANT)
    client_cloudant.connect()
    myDatabase = client_cloudant[DATABASE_NAME]
    if myDatabase.exists():
        print("'{0}' database is exist.\n".format(DATABASE_NAME))
    else:
        print("'{0}' database is not exist.\n".format(DATABASE_NAME))
    
    try:
        my_document = myDatabase[url_to_check["url"]]
        print("Url was exist in database '{0}' .\n".format(DATABASE_NAME))
        return {"website_is_ok":  my_document["website_is_ok"] }
    except:
        pass
        
    if filter_using_nlu(url_to_check["url"]) == False or filtering_with_visual_recognition == False:
        myDatabase.create_document({"_id": url_to_check["url"],"website_is_ok":  False})
        
    myDatabase.create_document({"_id": url_to_check["url"],"website_is_ok":  True})
    return { "website_is_ok" : True}
    