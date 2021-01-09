import React, { useState } from "react";
import ImageUploader from "react-images-upload";

const ImageUpload = (props) => {
    const [pictures, setPictures] = useState([]);

    const onDrop = (picture) => {
        setPictures([...pictures, picture]);
        console.log(picture);
    };
    return (
        <ImageUploader
            {...props}
            withIcon={true}
            onChange={onDrop}
            imgExtension={[".jpg", ".gif", ".png", ".gif"]}
            maxFileSize={5242880}
            withPreview={true}
        />
    );
};

export default ImageUpload;
