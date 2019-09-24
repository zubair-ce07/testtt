import {CardMedia} from "@material-ui/core";
import React from "react";
import Image from 'material-ui-image'

export const formatDate = date => {
    const options = {year: 'numeric', month: 'long', day: 'numeric'};
    return date.toLocaleDateString('en-US', options);
};
