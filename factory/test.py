from umeifactory import UMFactory
from ccfactory import CCFactory
from artfactory import ARTFactory

if __name__ == "__main__":
    url1 = "http://ccrt.cc/html/yazhou/"
    url2 = "http://www.umei.cc/p/gaoqing/gangtai/text_index-1.htm"
    url3 = "http://www.airenti.org/Html/Type/1_1.html"
    factory1 = CCFactory(url1)
    factory2 = UMFactory(url2)
    factory3 = ARTFactory(url3)