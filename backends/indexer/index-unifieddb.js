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

  const results = await Promise.all(
    els.map(async (el) => {
      const isFile = (await stat(path.resolve(localPath, el))).isFile();
      if (isFile) {
        const fileExt = path.extname(el);
        if ([".yaml", ".json"].includes(fileExt)) {
          const baseName = path.basename(el, fileExt);
          return { key: baseName, value: { $ref: path.join(...branch, el) } };
        }
      } else {
        const childNode = await rec([...branch, el], root);
        return { key: el, value: childNode };
      }
      return null;
    }),
  );

  for (const result of results) {
    if (result) {
      node[result.key] = result.value;
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
