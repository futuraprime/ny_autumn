import flickrapi
import process_image

class Photo:
    def __init__(self, photo_xml):
        attrs = photo_xml.attrib
        self.id = attrs['id']
        self.url = attrs['url_m']
        self.height = int(attrs['height_m'])
        self.width = int(attrs['width_m'])
        self.lat = float(attrs['latitude'])
        self.lng = float(attrs['longitude'])

    def process(self):
        self.colors = process_image.colorz(self.url)
        return self.colors

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

    photo_list = [Photo(el) for el in photos.find('photos').findall('photo')]

    return photo_list
