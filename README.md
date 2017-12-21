baidu_music_spider
# 百度音乐爬虫  我用的是python3 <br>
## 需求分析 <br>
- 1 首先需求就是爬去百度音乐列表里面的音乐    直白了就是拿到.mp3的url链接<br>
- 2 拿到百度音乐页面首先检测页面是否有.mp3的链接<br>
- 3 然后全局搜下.mp3 的相关信息   找到以下链接  返回json数据(包含一首歌的所有信息 作者名)<br>
http://tingapi.ting.baidu.com/v1/restserver/ting?method=baidu.ting.song.play&format=jsonp&callback=jQuery172011246684257020156_1510884252358&songid=100575177&_=1510884253110<br>
- 4 对此链接进行分析  删除 测试 看看次链接需要什么 发现只要携带歌曲id就行<br>
http://tingapi.ting.baidu.com/v1/restserver/ting?method=baidu.ting.song.play&songid={歌曲id}<br>
- 5 记得之前分析页面的时候有歌曲id的信息   很好   那么我们之爬取页面的id就行了<br>
- 6 写代码阶段  就三步<br>
- 7 一 提取页面歌曲id  然后拼接成json的url   接着就是下一页的url(查看是否完整需要拼接)   <br>
  二 对返回的json数据进行处理    提取需要的信息(作者名 歌名 歌曲的url(.mp3文件的url) 发行公司等等)<br>
  三 对歌曲的url进行请求  然接收到二进制歌曲文件  然后按照自己的方式保存<br>
### 安装依赖包<br>
> pip install -r requirements.txt<br>
### 运行爬虫<br>
> python main.py<br>
