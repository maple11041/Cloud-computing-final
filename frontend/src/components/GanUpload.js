import React, { useState } from "react";
import ImageUploader from "react-images-upload";
import { Button } from "react-bootstrap";
import axios from "axios";
import Result from "./Result";
import Spin from "./Spin";
import "./ImageUpload.css";

const GanUpload = (props) => {
    const API_URL = "http://localhost:5000";
    const [pictures, setPictures] = useState([]);
    const [status, setStatus] = useState("Upload");
    const [imgSrc, setImgSrc] = useState(null);

    const onDrop = (picture) => {
        setPictures([...pictures, picture]);
        // console.log(picture);
    };
    const upload = async (style) => {
        console.log(style);
        // console.log(pictures[0][0].name);
        // history.push("/result");
        try {
            let formData = new FormData();
            formData.append("file", pictures[0][0]);
            formData.append("filename", pictures[0][0].name);
            formData.append("style", style.toString());
            // console.log(pictures[0]);]
            // console.log("bbbbb");
            setStatus("Loading");
            const response = await axios.post(
                `${API_URL}/api/image/GanUpload`,
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
            <h1 className="header-wrapper">GAN Style Transfer</h1>
            <ImageUploader
                {...props}
                withIcon={true}
                onChange={onDrop}
                imgExtension={[".jpg", ".gif", ".png", ".gif"]}
                maxFileSize={5242880}
                withPreview={true}
            />
            <div className="upload-btn">
                <Button onClick={() => upload(0)}>WAVE</Button>
                <Button onClick={() => upload(1)} variant="secondary">
                    LA Muse
                </Button>
                <Button onClick={() => upload(2)} variant="success">
                    Rain Princess
                </Button>
                <Button onClick={() => upload(3)} variant="warning">
                    The Scream
                </Button>
                <Button onClick={() => upload(4)} variant="danger">
                    Udnie
                </Button>
                <Button onClick={() => upload(5)} variant="info">
                    Minotaur
                </Button>
            </div>
        </div>
    ) : status === "Loading" ? (
        <Spin />
    ) : (
        <Result imageSrc={imgSrc} />
    );
};

export default GanUpload;
