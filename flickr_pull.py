import flickrapi
import process_image

rtoh = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb))

def is_autumn_color(h,s,v):
    return h < 60 & 40 < s < 90 & 25 < v < 65

def average_rgbs(*args):
    avg = reduce(lambda memo, rgb: [a + b for a, b in zip(memo, rgb)], args)
    avg = [float(a) / float(len(args)) for a in avg]
    return (avg, len(args))

class PhotoList(list):
    def output(self):
        out = []
        for item in self:
            for color in item.autumn_color:
                out.append((color, item.lat, item.lng, item.id))
        return out

class Photo:
    def __init__(self, photo_xml):
        attrs = photo_xml.attrib
        self.id = attrs['id']
        self.url = attrs['url_m']
        self.height = int(attrs['height_m'])
        self.width = int(attrs['width_m'])
        self.lat = float(attrs['latitude'])
        self.lng = float(attrs['longitude'])
        self.process()

    def process(self):
        print 'processing... %s' % self.id
        self.colors = process_image.colorz(self.url)
        self.autumn_color = []
        for color in self.colors:
            if is_autumn_color(*color['hsv']):
                self.autumn_color.append(color)
        # autumn_avg = average_rgbs(autumn_color)
        return self.autumn_color


    def __repr__(self):
        return '<Photo id:%s lat:%f lng:%f>' % (self.id, self.lat, self.lng)

api_key = '4469375cfadd0f7ad76b2cd06400fb15'

flickr = flickrapi.FlickrAPI(api_key)

lat = 40.67
lng = -73.94
var = 0.5

def get_photos():
    photos = flickr.photos_search(
        tags='autumn, tree',
        bbox=','.join(map(str, [lat - var, lng - var, lat + var, lng + var])),
        media='photos',
        extras='url_m, geo',
    )

    photo_list = PhotoList()

    for el in photos.find('photos').findall('photo'):
        photo_list.append(Photo(el))

    return photo_list
