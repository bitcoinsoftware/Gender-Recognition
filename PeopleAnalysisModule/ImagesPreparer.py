import Image,  math
class ImagesPreparer:
        
    def prepare_trainning_csv_file(self,  output_file_url):
        file = open(output_file_url, "w")
        output_str = ""
        for preparing_elem in self.preparing_list:
            print preparing_elem
            output_str+=preparing_elem[0]  +";"#img src
            gender="0"
            if preparing_elem[1]["tags"][0]["attributes"]["gender"]["value"] =="female":  gender="1"
            output_str+=gender  +";"#gender 
            try:
                output_str+=str(preparing_elem[1]["tags"][0]["attributes"]["age_est"]["value"]) +";"#
            except:
                output_str+=str(preparing_elem[1]["tags"][0]["attributes"]["age_min"]["value"]*1.5) +";"#age
                
            output_str+=preparing_elem[1]["tags"][0]["attributes"]["mood"]["value"] +"\n"#mood
        file.write(output_str)
        file.close()
            
    def grayscale(self, image):
        image =image.convert("L")
        return image
            
    def Distance(self, p1,p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        return math.sqrt(dx*dx+dy*dy)

    def ScaleRotateTranslate(self,  image, angle, center = None, new_center = None, scale = None, resample=Image.BICUBIC):
        if (scale is None) and (center is None):
            return image.rotate(angle=angle, resample=resample)
        nx,ny = x,y = center[0], center[1]
        sx=sy=1.0
        if new_center:
            (nx,ny) = new_center
        if scale:
            (sx,sy) = (scale, scale)
        cosine = math.cos(angle)
        sine = math.sin(angle)
        a = cosine/sx
        b = sine/sx
        c = x-nx*a-ny*b
        d = -sine/sy
        e = cosine/sy
        f = y-nx*d-ny*e
        return image.transform(image.size, Image.AFFINE, (a,b,c,d,e,f), resample=resample)

                            #(self,image, eye_left_pix, eye_right_pix, offset_pct, size, output_image_name=image_url)
    def CropRotateFace(self,  image, eye_left=(0,0), eye_right=(0,0), offset_pct=(0.2,0.2), dest_sz = (180,180), output_image_name="default.jpg"):
        # calculate offsets in original image
        offset_h = math.floor(float(offset_pct[0])*dest_sz[0])
        offset_v = math.floor(float(offset_pct[1])*dest_sz[1])
        # get the direction
        eye_direction = (eye_right[0] - eye_left[0], eye_right[1] - eye_left[1])
        # calc rotation angle in radians
        rotation = -math.atan2(float(eye_direction[1]),float(eye_direction[0]))
        # distance between them
        dist = self.Distance(eye_left, eye_right)
        # calculate the reference eye-width
        reference = dest_sz[0] - 2.0*offset_h
        # scale factor
        scale = float(dist)/float(reference)
        # rotate original around the left eye
        image = self.ScaleRotateTranslate(image, center=eye_left, angle=rotation)
        # crop the rotated image
        crop_xy = (eye_left[0] - scale*offset_h, eye_left[1] - scale*offset_v)
        crop_size = (dest_sz[0]*scale, dest_sz[1]*scale)
        image = image.crop((int(crop_xy[0]), int(crop_xy[1]), int(crop_xy[0]+crop_size[0]), int(crop_xy[1]+crop_size[1])))
        # resize it
        image = image.resize(dest_sz, Image.ANTIALIAS)
        image = self.grayscale(image)
        image.save(output_image_name)


class ImagesPreparer2:
    def prepare_trainning_csv_file(self,  output_file_url):
        file = open(output_file_url, "w")
        output_str = ""
        for preparing_elem in self.preparing_list:
            print preparing_elem
            output_str+=preparing_elem[0]  +";"#img src
            gender="0"
            if preparing_elem[1]["tags"][0]["attributes"]["gender"]["value"] =="female":  gender="1"
            output_str+=gender  +";"#gender 
            try:
                output_str+=str(preparing_elem[1]["tags"][0]["attributes"]["age_est"]["value"]) +";"#
            except:
                output_str+=str(preparing_elem[1]["tags"][0]["attributes"]["age_min"]["value"]*1.5) +";"#age
                
            output_str+=preparing_elem[1]["tags"][0]["attributes"]["mood"]["value"] +"\n"#mood
        file.write(output_str)
        file.close()
            
    def grayscale(self, image):
        image =image.convert("L")
        return image
            
    def Distance(self, p1,p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        return math.sqrt(dx*dx+dy*dy)

    def ScaleRotateTranslate(self,  image, angle, center = None, new_center = None, scale = None, resample=Image.BICUBIC):
        if (scale is None) and (center is None):
            return image.rotate(angle=angle, resample=resample)
        nx,ny = x,y = center[0], center[1]
        sx=sy=1.0
        if new_center:
            (nx,ny) = new_center
        if scale:
            (sx,sy) = (scale, scale)
        cosine = math.cos(angle)
        sine = math.sin(angle)
        a = cosine/sx
        b = sine/sx
        c = x-nx*a-ny*b
        d = -sine/sy
        e = cosine/sy
        f = y-nx*d-ny*e
        return image.transform(image.size, Image.AFFINE, (a,b,c,d,e,f), resample=resample)

    def CropRotateFace(self,  image, eye_left=(0,0), eye_right=(0,0), offset_pct=(0.2,0.2), dest_sz = (180,180), output_image_name="default.jpg"):
        # calculate offsets in original image
        offset_h = math.floor(float(offset_pct[0])*dest_sz[0])
        offset_v = math.floor(float(offset_pct[1])*dest_sz[1])
        # get the direction
        eye_direction = (eye_right[0] - eye_left[0], eye_right[1] - eye_left[1])
        # calc rotation angle in radians
        rotation = -math.atan2(float(eye_direction[1]),float(eye_direction[0]))
        #if abs(rotation)>0.1 : rotation = 0
        # distance between them
        dist = self.Distance(eye_left, eye_right)
        # calculate the reference eye-width
        reference = dest_sz[0] - 2.0*offset_h
        # scale factor
        scale = float(dist)/float(reference)
        # rotate original around the left eye
        image = self.ScaleRotateTranslate(image, center=eye_left, angle=rotation)
        # crop the rotated image
        crop_xy = (eye_left[0] - scale*offset_h, eye_left[1] - scale*offset_v)
        crop_size = (dest_sz[0]*scale, dest_sz[1]*scale)
        image = image.crop((int(crop_xy[0]), int(crop_xy[1]), int(crop_xy[0]+crop_size[0]), int(crop_xy[1]+crop_size[1])))
        # resize it
        image = image.resize(dest_sz, Image.ANTIALIAS)
        image = self.grayscale(image)
        image.save(output_image_name)
        
    def CropFace(self, image,  offset_pct,  dest_sz,output_image_name="default.jpg"):
        # calculate offsets in original image
        offset_h = math.floor(float(offset_pct[0])*dest_sz[0])
        offset_v = math.floor(float(offset_pct[1])*dest_sz[1])
        # get the direction
        # calc rotation angle in radians
        rotation = 0
        # distance between them
        #dist = self.Distance(eye_left, eye_right)
        # calculate the reference eye-width
        reference = dest_sz[0] - 2.0*offset_h
        # rotate original around the left eye
        image = self.ScaleRotateTranslate(image, center=(0, 0), angle=rotation)
        # resize it
        image = image.resize(dest_sz, Image.ANTIALIAS)
        image = self.grayscale(image)
        image.save(output_image_name)
