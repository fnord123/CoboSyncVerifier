"use strict";

function error(error_info) {
  throw error_info;
}

function verifyUrheader(header) {
  if (header != "UR:BYTES") {
    error("Unknown header format");
  }
}

function verifySequence(sequence_text) {
  var sequence = sequence_text.split("OF");
  if (sequence.length != 2) {
    error("Invalid sequence format");
  }
  var index = sequence[0];
  if (index < 1) {
    error("Invalid sequence number");
  }
  var sequence_count = sequence[1];
  if (index > sequence_count) {
    error("Sequence number greater than sequence count");
  }
  return [index,sequence_count];
}

function checkEmptyFragment(fragment, index, fragments){
  if (fragment == undefined) {
    error("Missing expected fragment ${index}");
  }
}

function parseUr(ur_data) {
  var workloads = ur_data.split("\n");
  var fragments = new Array(workloads.length);
  var digest = "";
  var expectedPieces;
  workloads.forEach(parseWorkload, fragments);
  if (fragments.length < workloads.length) {
    error("Only detected ${fragments.length} out of expected ${workloads.length}");
  }
  return(fragments.join(""));

  function parseWorkload(value, index, array) {
    var pieces = value.split('/');
    if (pieces.length != 4) {
      error("Invalid format of line, should have four forward-slash separated pieces");
    }
    verifyUrheader(pieces[0]);
    var count = 0;
    [index, count] = verifySequence(pieces[1]);
    if (count != workloads.length) {
      error(`Header lists ${count} fragments but detected ${workloads.length} lines input`);
    }
    if (digest == "") {
      digest = pieces[2];
    } else if (digest != pieces[2]) {
      error("Invalid workload, digest changed");
    }
    var payload = pieces[3];
    if (fragments[index-1] == undefined) {
      fragments[index-1] = payload;
    } else if (fragments[index-1] != payload) {
      error("Invalid workload, payload changed");
    }
  }
}

export { parseUr };
