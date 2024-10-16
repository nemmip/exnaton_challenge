import React from 'react';
import {Select, Space, Typography} from "antd";
import Tags from "../../interfaces/Tags.ts";


const DataSelectBar: React.FC<{
    tags: Tags[]
    onChange: void
}> = ({tags, onChange}) => {

    return (
        <div>
            <Typography.Text>Select data for: </Typography.Text>
            <Space/>
            <Select style={{width: '80%'}} onChange={onChange}>
                {tags.map(el => <Select.Option key={el.id} value={el.id}>{el.muid}</Select.Option>)}
            </Select>
        </div>
    );
};

export default DataSelectBar;