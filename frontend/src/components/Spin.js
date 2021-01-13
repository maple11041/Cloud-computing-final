import { Spinner } from "react-bootstrap";
const Spin = () => {
    return (
        <div className="spinner-wrapper">
            <Spinner animation="border" role="status">
                <span className="sr-only">Loading...</span>
            </Spinner>
        </div>
    );
};

export default Spin;
