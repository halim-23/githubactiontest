odoo.define("web_mobile.testUtils", function () {
  "use strict";

  /**
   * Transforms base64 encoded data to a Blob object
   *
   * @param {String} b64Data
   * @param {String} contentType
   * @param {int} sliceSize
   * @returns {Blob}
   */
  function base64ToBlob(b64Data, contentType, sliceSize) {
    contentType = contentType || "";
    sliceSize = sliceSize || 512;

    const byteCharacters = atob(b64Data);
    const byteArrays = [];

    for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
      const slice = byteCharacters.slice(offset, offset + sliceSize);
      const byteNumbers = Array.from(slice).map((char) => char.charCodeAt(0));
      byteArrays.push(new Uint8Array(byteNumbers));
    }

    return new Blob(byteArrays, {type: contentType});
  }

  return {
    base64ToBlob,
  };
});
