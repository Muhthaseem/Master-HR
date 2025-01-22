const mongoose = require("mongoose");


const locationSchema = new mongoose.Schema({

  HR:{
        type:mongoose.Schema.Types.ObjectId,
        ref:'HR',
        required:true
       },

  coords: {
    accuracy: { type: Number, required: true },
    altitude: { type: Number, required: true },
    altitudeAccuracy: { type: Number, required: true },
    heading: { type: Number, required: true },
    latitude: { type: Number, required: true },
    longitude: { type: Number, required: true },
    speed: { type: Number, required: true }
  },
  mocked: { type: Boolean, required: true },
  timestamp: { type: Date, required: true, get: (v) => new Date(v) }

});

// Create a model from the schema
const Location = mongoose.model("Location", locationSchema);

module.exports = Location;
