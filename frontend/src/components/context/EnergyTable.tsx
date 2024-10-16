import React from 'react';
import {Table} from "antd";
import Measurement from "../../interfaces/Measurement.ts";

const EnergyTable: React.FC<{
    data: Measurement[]
}> = ({data}) => {

    const columns = [
        {
            title: 'Id',
            dataIndex: 'id',
            key: 'id',
        },
        {
            title: 'Measurement',
            dataIndex: 'measurement',
            key: 'measurement',
        },
        {
            title: 'Energy',
            dataIndex: 'energy',
            key: 'energy',
        },
        {
            title: 'Timestamp',
            dataIndex: 'timestamp',
            key: 'timestamp',
            render: (el) => (new Date(el)).toUTCString()
        },
    ];

    return (
        <div>
            <Table dataSource={data} columns={columns}/>;
        </div>
    );
};

export default EnergyTable;