const express=require('express');
const jwt=require('jsonwebtoken')
const router=express.Router();
require('dotenv').config();

const SECRET=process.env.JWT_SECRET;
const USERS={parshwa:"1235",admin:"admin_123"};

router.post('/login',(req,res)=>{
    const{username,password}=req.body;
    if(USERS[username]==password)
    {
        const token=jwt.sign({username},SECRET,{expiresIn:'1h'});
        console.log("Token: ",token);
        return res.json({token});
    }
    res.status(401).json({error:'Invalid Username or Password!'});
});

module.exports=router;