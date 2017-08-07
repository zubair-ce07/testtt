function replaceDirects(name, json, directs) {
  if (json.name === name) {
    let newJson = {};
    Object.assign(newJson, json);
    newJson.directs = directs;
    return newJson;
  } else {
    return {
      name: json.name,
      directs: json.directs
        ? json.directs.map(current => replaceDirects(name, current))
        : null
    };
  }
}

let utils = {
  replaceDirects
};

export default utils;
