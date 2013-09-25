import flickrapi

api_key = '4469375cfadd0f7ad76b2cd06400fb15'

flickr = flickrapi.FlickrAPI(api_key)

lat = 40.67
lng = -73.94
var = 0.5

photos = flickr.photos_search(
    tags='autumn, tree',
    bbox=','.join(map(str, [lat - var, lng - var, lat + var, lng + var])),
    media='photos',
    extras='url_m',
)

print len(photos.find('photos').findall('photo'))
