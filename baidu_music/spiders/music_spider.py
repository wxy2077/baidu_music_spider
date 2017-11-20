# -*- coding: utf-8 -*-
# @author:wg
import json
import os

import scrapy
from copy import deepcopy

import time


# 需求分析
# 1 首先需求就是爬去百度音乐列表里面的音乐    直白了就是拿到.mp3的url链接
# 2 拿到百度音乐页面首先检测页面是否有.mp3的链接
# 3 然后全局搜下.mp3 的相关信息   找到以下链接  返回json数据(包含一首歌的所有信息 作者名)
# http://tingapi.ting.baidu.com/v1/restserver/ting?method=baidu.ting.song.play&format=jsonp&callback=jQuery172011246684257020156_1510884252358&songid=100575177&_=1510884253110
# 4 对此链接进行分析  删除 测试 看看次链接需要什么 发现只要携带歌曲id就行
# http://tingapi.ting.baidu.com/v1/restserver/ting?method=baidu.ting.song.play&songid={歌曲id}
# 5 记得之前分析页面的时候有歌曲id的信息   很好   那么我们之爬取页面的id就行了
# 6 写代码阶段  就三步
# 7  一 提取页面歌曲id  然后拼接成json的url   接着就是下一页的url(查看是否完整需要拼接)
#    二 对返回的json数据进行处理    提取需要的信息(作者名 歌名 歌曲的url(.mp3文件的url) 发行公司等等)
#    三 对歌曲的url进行请求  然接收到二进制歌曲文件  然后按照自己的方式保存

class MusicSpiderSpider(scrapy.Spider):
    name = "music_spider"
    allowed_domains = ["baidu.com"]
    start_urls = [
        # 起始url是以流行音乐为关键词搜索的
        'http://music.baidu.com/tag/%E6%B5%81%E8%A1%8C',
    ]

    def parse(self, response):

        item = {}
        # 获取音乐的url列
        mp3_href_list = response.xpath("//span[@class='song-title']/a[1]/@href").extract()
        # 从音乐的url列表中提取出id号
        mp3_id_list = [i.split('/')[-1] for i in mp3_href_list]
        # 组合成新的json_url
        for id in mp3_id_list:
            json_url = 'http://tingapi.ting.baidu.com/v1/restserver/ting?method=baidu.ting.song.play&songid=' + id
            # print(json_url)
            yield scrapy.Request(
                json_url,
                self.parse_mp3,
                meta={"item": deepcopy(item)}
            )
        # print(mp3_id_list)
        # print("-" * 50)
        # 获取下一页url 获取的值是列表
        next_url = response.xpath("//a[@class='page-navigator-next']/@href").extract()

        time.sleep(20)  # 网速太慢解析完一页之后缓冲下等待下载歌曲
        if next_url:  # 表示有下一页的url
            # 拼接下一页完整url
            next_url = "http://music.baidu.com" + next_url[0].strip()
            # 解析下一页url
            yield scrapy.Request(
                next_url,
                callback=self.parse,
            )


    def parse_mp3(self, response):
        """解析mp3的url   返回json数据格式"""
        item = response.meta['item']

        # 获取到歌曲的json数据    要经过以下处理
        content = json.loads(response.body_as_unicode())

        # 提取歌曲的相关信息
        item['author'] = content['songinfo']['author']
        item['song_name'] = content['songinfo']['title']
        item['song_href'] = content['bitrate']['show_link']
        # 解析
        yield scrapy.Request(
            item['song_href'],
            callback=self.parse_mp3_href,
            meta={"item": deepcopy(item)},
        )

    def parse_mp3_href(self, response):
        """获取mp3的二进制数据"""
        item = response.meta['item']
        # print(item)
        # 判断路径是否存在
        if not os.path.exists("./song/"):
            # 不存在自动建立
            os.makedirs("./song/")
            # 以歌曲名--作者的 方式保存 记住是wb　本来是要在pipelines里面保存的  保存二进制文件
        with open("./song/" + item['song_name'] + "--" + item['author'] + ".mp3", "wb") as f:
            # 保存歌曲
            f.write(response.body)
            print("保存成功---%s" % item['song_name'])
