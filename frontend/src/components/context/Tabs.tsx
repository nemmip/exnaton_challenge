import React, {useEffect, useState} from 'react';
import {Tabs as TabsAntd, TabsProps, Typography} from "antd";
import EnergyTable from "./EnergyTable.tsx";
import Tags from "../../interfaces/Tags.ts";
import EnergyChart from "./Energy/EnergyChart.tsx";
import EnergyOptions from "./Energy/EnergyOptions.tsx";

const Tabs: React.FC<{
    tag: Tags
}> = ({tag}) => {
    const [data, setData] = useState([])
    useEffect(() => {
        if (tag)
            fetch(`http://localhost:5001/measurements/?tags_id=${tag}`).then(res => res.json())
                .then(data => setData(data.map(el => ({key: el.id, ...el}))))
    }, [tag]);



    const items: TabsProps['items'] = [
        {
            key: '1',
            label: 'Table',
            children: <EnergyTable data={data}/>,
        },
        {
            key: '2',
            label: 'Chart',
            children: data.length ?
                // <EnergyChart data={data} average={averageValue[0].operation_value}/> :
                <EnergyOptions data={data} tag={tag}/> :
                <Typography.Text>No data selected</Typography.Text>,
        },
    ];
    return (
        <>
            <TabsAntd
                defaultActiveKey="1"
                items={items}
                size='large'
            />
        </>
    );
};

export default Tabs;