import React, {useEffect, useState} from 'react';
import {DatePicker} from "antd";
import dayjs from "dayjs";
import Measurement from "../../../interfaces/Measurement.ts";
import EnergyChart from "./EnergyChart.tsx";

const EnergyOptions: React.FC<{
    data: Measurement[],
    tag: number
}> = ({data, tag}) => {
    const defaultQuery = `http://localhost:5001/analytics/measurement?field_name=energy&operation=avg&tags_id=${tag}`
    const [selectedDate, setSelectedDate] = useState<dayjs.Dayjs>(null)
    const [averageValue, setAverageValue] = useState(null)
    const [queryString, setQueryString] = useState(defaultQuery)
    const [filteredData, setFilteredData] = useState(data)
    useEffect(() => {
        if (!selectedDate){
            setQueryString(defaultQuery)
        }
        else {
            setQueryString(defaultQuery + `&date=${selectedDate.format('YYYY-MM-DD')}`)
        }
    }, [selectedDate, tag]);

    useEffect(() => {
        fetch(queryString).then(res => res.json())
            .then(data => setAverageValue(data))
    }, [queryString]);

    useEffect(() => {
        if(!selectedDate){
            setFilteredData(data)
        }else{
            setFilteredData(data.filter(el=> el.timestamp.startsWith(selectedDate.format('YYYY-MM-DD'))))
        }
    }, [selectedDate, data]);
    return (
        averageValue && <>
            <DatePicker value={selectedDate} onChange={(date)=> setSelectedDate(date)}/>
            <EnergyChart data={filteredData} average={averageValue[0].operation_value}/>
        </>
    );
};

export default EnergyOptions;