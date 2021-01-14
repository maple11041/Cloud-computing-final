import React, { useState } from "react";
import ImageUploader from "react-images-upload";
import { Button } from "react-bootstrap";
import axios from "axios";
import Result from "./Result";
import Spin from "./Spin";
import "./ImageUpload.css";

const ImageUpload = (props) => {
    const API_URL = "http://localhost:5000";
    const [pictures, setPictures] = useState([]);
    const [status, setStatus] = useState("Upload");
    const [imgSrc, setImgSrc] = useState(null);

    const onDrop = (picture) => {
        setPictures([...pictures, picture]);
        // console.log(picture);
    };

    const upload = async (style) => {
        // console.log("test");
        console.log(style);
        // console.log(pictures[0][0].name);
        // history.push("/result");
        try {
            let formData = new FormData();
            formData.append("file", pictures[0][0]);
            formData.append("filename", pictures[0][0].name);
            formData.append("style", style);
            // console.log(pictures[0]);]
            // console.log("bbbbb");
            setStatus("Loading");
            const response = await axios.post(
                `${API_URL}/api/image/upload`,
                formData
            );
            // console.log(response.data);
            // var file = new Blob([response.data], { type: "image/jpg" });
            // console.log(response.data);
            // console.log(response.data.image);
            setImgSrc(response.data.image);
            // console.log(file);
            // let fileReader = new FileReader();
            // fileReader.readAsDataURL(file);
            // fileReader.onload = () => {
            //     let result = fileReader.result;
            //     // console.log(result);
            //     setImgSrc(result);
            // };
            // console.log("aaaaa");
            setStatus("Result");
        } catch (error) {
            console.log(error);
        }
    };
    return status === "Upload" ? (
        <div className="upload-wrapper">
            <h1 className="header-wrapper">Style Transfer</h1>
            <ImageUploader
                {...props}
                withIcon={true}
                onChange={onDrop}
                imgExtension={[".jpg", ".gif", ".png", ".gif"]}
                maxFileSize={5242880}
                withPreview={true}
            />
            {pictures.length !== 0 ? (
                <>
                    <h2 className="header-wrapper">
                        Please choose the style you want to transfer
                    </h2>
                    <div className="upload-btn">
                        <Button onClick={() => upload("for-mosaic")}>
                            Mosiac
                        </Button>
                        <Button
                            variant="secondary"
                            onClick={() => upload("for-contract")}
                        >
                            Contract
                        </Button>
                        <Button
                            variant="success"
                            onClick={() => upload("for-sharp")}
                        >
                            Sharpen
                        </Button>
                        <Button
                            variant="warning"
                            onClick={() => upload("for-inv")}
                        >
                            Inverse
                        </Button>
                        <Button
                            onClick={() => upload("for-text")}
                            variant="danger"
                        >
                            Signature
                        </Button>
                    </div>
                </>
            ) : null}
        </div>
    ) : status === "Loading" ? (
        <Spin />
    ) : (
        <Result imageSrc={imgSrc} />
    );
};

export default ImageUpload;
