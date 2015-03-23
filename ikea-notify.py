# -*- coding: utf-8 -*-
import datetime
import requests
from xml.etree import ElementTree
 
# \n릴나겐 유리닦이 202.435.97 / 직원문의\n링셴 샤워커튼링 001.793.90 / 직원문의\n에게그룬드 샤워커튼 902.094.39 / 직원문의\n고드모르곤 양문형 거울장(총 3짝 사야함, 옆에 붙어있어도 문이 열리는지 확인) 702.189.96 / 직원문의\n알렉스 서랍유닛 801.928.25 / 11.19\n칼뷔 조리대 (나무 3종) 202.971.18 / 직원문의\n로그룬드 휴지스탠드 102.530.73 / 직원문의\n세베른 샤워 커튼봉 701.667.99 / 직원문의\n롱란 거울 402.886.98 / 직원문의\n오플란트 4칸 서랍장 302.691.53 / 품절\n오플란드 2칸 서랍장 202.691.44 / 직원문의\n드라간 욕실 수납함 2종 202.226.08 / 직원문의\n임멜른 비누받침 902.526.25 / 직원문의\n몰게르 거울 (80*60) 602.304.99 / 44.10\n비테묄라 벽부착등 102.835.03 / 품절\n(몰게르 벽선반이 없으면) 몰게르 선반장 702.673.93 / 32.10\n몰게르 벽선반 802.423.59 / 44.04\n".match(/(\d+\.\d+.\d+)/g).map(function(e){e.split('.').join('')})

# TODO: either item name or id should be ok
# item_ids = ["20243597", "00179390", "90209439", "70218996", "80192825", "20297118", "10253073", "70166799", "40288698", "30269153", "20269144", "20222608", "90252625", "60230499", "10283503", "70267393", "80242359", "40249961"]
item_ids = ["20243597"]

item_url_template = 'http://www.ikea.com/{region}/{locale}/catalog/products/{item_id}/?type=xml&dataset=normal'
availability_url_template = 'http://www.ikea.com/{region}/{locale}/iows/catalog/availability/{item_id}'

def find_from_xml_str(tree, tagname, post_filter=None):
    for expected in tree.iter(tagname):
        return post_filter(expected.text) if post_filter else expected.text

def query(item_ids, region='kr', locale='ko'):
    query_result = []  # item_id, item_availability, validDate
    # Perform xml queries and parse
    for item_id in item_ids:
        item_data = requests.get(item_url_template.format(region=region, locale=locale, item_id=item_id))
        availability_data = requests.get(availability_url_template.format(region=region, locale=locale, item_id=item_id))

        item_tree = ElementTree.fromstring(item_data.content)
        availability_tree = ElementTree.fromstring(availability_data.content)

        available_qty = find_from_xml_str(availability_tree, 'availableStock', int)
        valid_date = find_from_xml_str(availability_tree, 'validDate', lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
        item_name = find_from_xml_str(item_tree, 'name')
     
        query_result.append((item_id, available_qty, valid_date))
 
    print query_result

query(item_ids)

