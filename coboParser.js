import { parseUr } from './urProtocol.js';

function error(error_info) {
  throw error_info;
}

function parse_qr_text(input) {
  var input_area = document.getElementById("coboQrText");
  input = input_area.value;
  // Remove any extra blank lines and carriage returns the user may have
  // input by mistake.
  var cleaned_input = input.replace(/^(?=\n)$|^\s*|\s*$|\n\n+/gm,"");
  var ur_payload = parseUr(cleaned_input);
  console.log(ur_payload);
}
window.parse_qr_text = parse_qr_text;
