const express=require("express");
const Router=express.Router();

const Location = require("../Models/LocationSchema");


Router.post("/",(req,res)=>{
    
    const locationData = req.body;

    
      // Create a new Location document using the request body data
      const newLocation = new Location({
        HR:locationData.HR,
        coords: locationData.coords,
        mocked: locationData.mocked,
        timestamp:locationData.timestamp, // Convert to Date if necessary
      });
  

    newLocation.save().then(()=>{
        res.status(200).json({message:"Location Added"})
    })
    .catch((err)=>{res.status(500).json({message:"Error",err})})

})




Router.get('/hr/:HR',async (req,res)=>{

  const{HR}=req.params

  try{
     const location=await Location.find({HR})
     console.log(location)
     if(!location){
        return res.status(404).json({message:"No location found"})
     }
     res.status(200).json(location)


  }
  catch(err){
     res.status(500).json({message:"Error fetching location"})
     console.log(err)
  }
})




module.exports=Router;