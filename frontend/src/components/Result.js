import React from "react";
import testImg from "./test.jpg";
import "./Result.css";

const Result = ({ imageSrc }) => {
    // console.log(update);
    return (
        <div className="image-wrapper">
            <img src={`data:image/jpg;base64,${imageSrc}`} />
            <img src={`data:image/jpg;base64,${imageSrc}`} />
        </div>
    );
};
export default Result;
