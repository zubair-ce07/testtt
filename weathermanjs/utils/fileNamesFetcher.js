import {months} from "./constants";
import glob from "glob";

export const getFileNames = (path, raw_date) => {
    const date = new Date(raw_date);
    const pattern = `${date.getFullYear()}_${months[date.getMonth()] || ''}`;
    const options = {cwd: path};
    return glob.sync(`*${pattern}*`, options);
};