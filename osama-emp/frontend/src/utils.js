function replaceDirects(name, hierarchy, directs) {
  if (hierarchy.username === name) {
    return Object.assign({}, hierarchy, {
      directs
    });
  } else {
    return Object.assign({}, hierarchy, {
      directs: hierarchy.directs
        ? hierarchy.directs.map(current =>
            replaceDirects(name, current, directs)
          )
        : []
    });
  }
}

function findInHierarchy(name, hierarchy) {
  if (hierarchy.username === name) {
    return hierarchy;
  } else {
    return hierarchy.directs.map(current => findInHierarchy(name, current));
  }
}

let utils = {
  replaceDirects,
  findInHierarchy
};

export default utils;
