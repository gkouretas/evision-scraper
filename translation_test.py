import translators as ts

text = 'gripe'
test = ts.google(text)
print(test)
# chs_text = '季姬感到寂寞，罗集了一些鸡来养，鸡是那种出自荆棘丛中的野鸡。野鸡饿了唧唧叫，季姬就拿竹箕中的谷物喂鸡。'
# html_text = '''
# <!DOCTYPE html>
# <html>
# <head>
# 	<title>我是标题</title>
# </head>
# <body>
# <p>我是文章《你的父亲》</p>
# </body>
# </html>
# '''

# # input languages
# print(ts.google(wyw_text)) # default: from_language='auto', to_language='en'

# ## output language_map
# print(ts._google.language_map)

# # professional field
# # print(ts.alibaba(wyw_text, professional_field='general')) # ("general","message","offer")
# # print(ts.baidu(wyw_text, professional_field='common')) # ('common','medicine','electronics','mechanics')
# # print(ts.caiyun(wyw_text, from_language='zh', professional_field=None)) # ("medicine","law","machinery")

# # # property
# # rs = [ts.tencent(x) for x in [wyw_text, chs_text]]
# # print(ts._tencent.query_count)
# # print(dir(ts._tencent))

# # # requests
# # print(ts.youdao(wyw_text, sleep_seconds=5, proxies={}))

# # # host service
# # print(ts.google(wyw_text, if_use_cn_host=True))
# # print(ts.bing(wyw_text, if_use_cn_host=False))

# # # detail result
# # print(ts.sogou(wyw_text, is_detail_result=True))

# # # translate html
# # print(ts.translate_html(html_text, translator=ts.google, to_language='en', n_jobs=-1))

# # # help
# # help(ts.google)
