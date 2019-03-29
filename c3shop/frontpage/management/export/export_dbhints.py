import base64
import traceback

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, StreamingHttpResponse

from frontpage.management.magic import timestamp
from frontpage.management.mediatools.media_actions import PATH_TO_UPLOAD_FOLDER_ON_DISK
from frontpage.models import Media, Article, Post


class DataDumpIterator:

    step: int = 8
    ip: str = ""
    payload = None

    def __iter__(self):
        self.step = 8
        self.payload = None
        return self

    def __init__(self, ipaddr: str):
        super().__init__()
        self.ip = ipaddr

    def __next__(self):
        if self.step == 0:
            raise StopIteration
        if self.step == 1:
            return "# IP: " + str(self.ip)
        elif self.step == 8:
            # Return stored images
            if self.payload is None:
                self.payload = 1  # Look up first id
            try:
                img = Media.objects.get(id=int(self.payload))
                a = '{"type" : "media", "data" : [ "category" : "'
                a += str(base64.b64encode(bytes(str(img.category), 'utf-8'))) + '", "headline" : "'
                a += str(base64.b64encode(bytes(str(img.headline), 'utf-8'))) + '", "text" : "'
                a += str(base64.b64encode(bytes(str(img.text), 'utf-8'))) + '", "timestamp" : "'
                # We'll not save the cached text here as it can be recreated
                a += str(base64.b64encode(bytes(str(img.uploadTimestamp), 'utf-8'))) + '", "highfilepath" : "'
                a += str(base64.b64encode(bytes(str(img.highResFile), 'utf-8'))) + '", "lowfilepath" : "'
                a += str(base64.b64encode(bytes(str(img.lowResFile), 'utf-8'))) + '", "highresfile" : "'
                f = open(PATH_TO_UPLOAD_FOLDER_ON_DISK + str(img.highResFile)[1:], "rb") # remove trailing /
                a += str(base64.b64encode(f.read())) + '", "lowresfile" : "'
                f.close()
                f = open(PATH_TO_UPLOAD_FOLDER_ON_DISK + str(img.lowResFile)[1:], "rb")
                a += str(base64.b64encode(f.read())) + '"]}\n'
                f.close()
                self.payload = int(self.payload) + 1
                return a
            except ObjectDoesNotExist:
                self.step -= 1
                self.payload = None
                return "#\n# We're finished with the media assets. Moving on...\n#\n"
            except Exception as e:
                self.step -= 1
                self.payload = None
                return "# Hit an exception. Assuming that we reached the end of the media assets.\n" \
                        "# Exception content: " + str(e).replace("\n", "") + "\n" \
                       + traceback.format_exc().replace("\n", "\n# ")
            pass
        elif self.step == 7:
            # Return articles
            if self.payload is None:
                self.payload = 1 # Look up first id
            try:
                art = Article.objects.get(id=int(self.payload))
                a = '{"type" : "article", "data" : [ "price" : "'
                a += str(base64.b64encode(bytes(str(art.price), 'utf-8'))) + '", "largeText" : "'
                a += str(base64.b64encode(bytes(str(art.largeText), 'utf-8'))) + '", "type" : "'
                a += str(base64.b64encode(bytes(str(art.type), 'utf-8'))) + '", "description" : "'
                a += str(base64.b64encode(bytes(str(art.description), 'utf-8'))) + '", "visible" : "'
                a += str(base64.b64encode(bytes(str(art.visible), 'utf-8'))) + '", "quantity" : "'
                a += str(base64.b64encode(bytes(str(art.quantity), 'utf-8'))) + '", "size" : "'
                a += str(base64.b64encode(bytes(str(art.size), 'utf-8'))) + '", "addedby" : "'
                try:
                    a += str(base64.b64encode(bytes(str(art.addedByUser.authuser.username), 'utf-8'))) + '", "flashimgid" : "'
                except Exception as e:
                    print(e)
                    a += str(base64.b64encode(bytes(str("admin"), 'utf-8'))) + '", "flashimgid" : "'
                try:
                    a += str(base64.b64encode(bytes(str(art.flashImage.id), 'utf-8'))) + '", "chestsize" : "'
                except:
                    a += str(base64.b64encode(bytes(str("none"), 'utf-8'))) + '", "chestsize" : "'
                a += str(base64.b64encode(bytes(str(art.chestsize), 'utf-8'))) + '"]}\n'
                self.payload = int(self.payload) + 1
                return a
            except ObjectDoesNotExist:
                self.step -= 1
                self.payload = None
                return "#\n# We're done with the articles. Moving on...\n#\n"
            except Exception as e:
                self.step -= 1
                self.payload = None
                return "# There was an exception while processing the articles. Jumping to the next job.\n" \
                        "# Exception content: " + str(e).replace("\n", "") + "\n" + \
                       traceback.format_exc().replace("\n", "\n# ")
        elif self.step == 6:
            # Saving posts to data dump
            if self.payload is None:
                self.payload = 1
            try:
                p = Post.objects.get(id=1)
                a = '{"type" : "post", "data" : [ "title" : "'
                a += str(base64.b64encode(bytes(str(p.title), 'utf-8'))) + '", "addedby" : "'
                try:
                    a += str(base64.b64encode(bytes(str(p.createdByUser.authuser.username), 'utf-8'))) + \
                         '", "username" : "'
                except Exception as e:
                    a += str(base64.b64encode(bytes(str("admin"), 'utf-8'))) + '", "visible" : "'
                a += str(base64.b64encode(bytes(str(p.visibleLevel), 'utf-8'))) + '", "timestamp" : "'
                a += str(base64.b64encode(bytes(str(p.timestamp), 'utf-8'))) + '", "text" : "'
                a += str(base64.b64encode(bytes(str(p.text), 'utf-8'))) + '"]}\n'
                return a
            except ObjectDoesNotExist as e:
                self.step -= 1
                self.payload = None
                return "#\n# We're done with the posts. Moving on...\n#\n"
            except Exception as e:
                self.step -= 1
                self.payload = None
                return "# There was an exception while processing the posts. Jumping to the next job.\n" \
                        "# Exception content: " + str(e).replace("\n", "") + "\n" + \
                       traceback.format_exc().replace("\n", "\n# ")
        else:
            # something went wrong
            if self.step < 0:
                self.step = 0
                return StopIteration
            self.step -= 1
            return self.__next__()


def get_dump_iterator(ip: str):
    return iter(DataDumpIterator(ip))


def request_data_dump(request: HttpRequest) -> StreamingHttpResponse:
    response: StreamingHttpResponse = StreamingHttpResponse(get_dump_iterator(request.META.get('REMOTE_ADDR')))
    response['Content-Type'] = 'application/focdump-demformat'
    response['Content-Disposition'] = 'attachment; filename="c3foc-datadump-' + timestamp() + '.pxtz"'
    return response
