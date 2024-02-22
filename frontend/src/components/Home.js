import Carousel from "react-bootstrap/Carousel";

const Home = () => {
    return (
        <div className="row">
            <Carousel variant="dark">
                <Carousel.Item>
                    <img
                        className="d-block w-100"
                        src={
                            "https://wespirebackend.s3.ap-southeast-1.amazonaws.com/media/slide01.134836f0554d2499338e.jpg"
                        }
                        alt="First slide"
                    />
                </Carousel.Item>
                <Carousel.Item>
                    <img
                        className="d-block w-100"
                        src={
                            "https://wespirebackend.s3.ap-southeast-1.amazonaws.com/media/slide02.78166f20310a125a5405.jpg"
                        }
                        alt="Second slide"
                    />
                </Carousel.Item>
                <Carousel.Item>
                    <img
                        className="d-block w-100"
                        src={
                            "https://wespirebackend.s3.ap-southeast-1.amazonaws.com/media/slide03.10bade9f35d98f6aa3df.jpg"
                        }
                        alt="Third slide"
                    />
                </Carousel.Item>
            </Carousel>
        </div>
    );
};

export default Home;
