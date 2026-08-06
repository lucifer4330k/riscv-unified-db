#!/usr/bin/env node
"use strict";

const process = require("process");
const path = require("path");
const fs = require("fs");

const { readdir, stat } = fs.promises;

const rec = async (branch, root) => {
  const node = {};
  const localPath = path.resolve(root, ...branch);
  const els = await readdir(localPath);

  const promises = els.map(async (el) => {
    const isFile = (await stat(path.resolve(localPath, el))).isFile();
    const fileExt = path.extname(el);
    const baseName = path.basename(el, fileExt);
    if (isFile) {
      if ([".yaml", ".json"].includes(fileExt)) {
        return { key: baseName, val: { $ref: path.join(...branch, el) } };
      }
    } else {
      const childNode = await rec([...branch, el], root);
      return { key: el, val: childNode };
    }
    return null;
  });

  const results = await Promise.all(promises);

  for (const res of results) {
    if (res) {
      node[res.key] = res.val;
    }
  }
  return node;
};

const main = async () => {
  const [, , root] = process.argv;
  if (root === undefined) {
    console.error(
      "usage: ./index-unifieddb.js <path-to-unifieddb-arch-folder>",
    );
    return;
  }
  const rootPath = path.resolve(".", root);
  const tree = await rec([], rootPath);
  console.log(JSON.stringify(tree, null, 2));
};

main();
