import React, {useEffect, useState} from 'react';
import Tabs from "./context/Tabs.tsx";
import {Col, Row} from "antd";
import DataSelectBar from "./context/DataSelectBar.tsx";

const Context: React.FC = () => {
    const [tags, setTags] = useState([])
    const [selectedTag, setSelectTag] = useState(null)
    useEffect(() => {
        fetch('http://localhost:5001/tags/').then(res => res.json()).then(data => setTags(data))
    }, []);

    const handleSelectTag = (tag) => {
        setSelectTag(tag)
    }

    return (
        <>
            <Row>
                <Col span={12}>
                    <DataSelectBar tags={tags} onChange={handleSelectTag}/>
                </Col>
            </Row>
            <Row>
                <Col span={24}>
                    <Tabs tag={selectedTag}/>
                </Col>
            </Row>
        </>
    )
};

export default Context;