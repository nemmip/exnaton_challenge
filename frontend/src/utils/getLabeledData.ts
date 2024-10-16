import Measurement from "../interfaces/Measurement.ts";
import getUniqueDates from "./getUniqueDates.ts";
import {format} from 'date-fns';

export default function getLabeledData(data: Measurement[]) {
    const uniqueDates = getUniqueDates(data)
    const labeledData = uniqueDates.map(date => {
        return {
            label: date,
            data: data.filter(el => (new Date(el.timestamp)).toLocaleDateString() === date)
                .map(el => {
                    return {
                        time: format((new Date(el.timestamp)), "HH:mm"),
                        energy: el.energy
                    }
                })
        }
    })
    return labeledData
}