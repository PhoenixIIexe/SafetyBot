import React, { useRef, useEffect } from 'react';

const Camera = () => {
    const videoRef = useRef(null);

    useEffect(() => {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                videoRef.current.srcObject = stream;
                videoRef.current.play();
            })
            .catch(function (err) {
                console.log('Error: ' + err);
            });
    }, []);

    return (
        <div>
            <video ref={videoRef} />
        </div>
    );
};

export default Camera;