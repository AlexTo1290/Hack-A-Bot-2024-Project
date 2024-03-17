import React, { useState, useEffect } from 'react';

const Log = () => {
    const [data, setData] = useState(null);

    useEffect(() => {
        const intervalId = setInterval(() => {
            fetch('localhost:3000/logs')
                .then((res) => {
                return res.json();
                })
                .then((data) => {
                setData(data);
                });
        }, 300)

        return () => clearInterval(intervalId);

    }, []);

    return (<>
    
    </>)
}

export default Log;