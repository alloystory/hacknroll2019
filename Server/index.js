const express = require("express")
const multer = require("multer")
const Sequelize = require('sequelize')
const Op = Sequelize.Op
const Joi = require('joi')

// General Config
const host = "127.0.0.1"
const port = process.env.PORT || 9000

// Express Config
const app = express()
app.use(express.json())

// Sequelize Config
const db = new Sequelize('hacknroll2019', 'root', '', {
  host: host,
  dialect: 'mysql',
  operatorsAliases: false,

  pool: {
    max: 5,
    min: 0,
    acquire: 30000,
    idle: 10000
  },
})

// Multer Config
const storage = multer.diskStorage({
	destination: "./uploads",
	filename: function (req, file, callback){
		callback(null, req.params.filename)
	}
})
const upload = multer({storage: storage}).single("img")

// Joi Config
const schema = {
	name: Joi.string().min(3).required(),
	description: Joi.string().min(3).required(),
	rating: Joi.number().required(),
	category_id: Joi.number().required(),
	provider: Joi.string().min(3).required(),
	price: Joi.number().required(),
	image: Joi.required(),
	url: Joi.string().min(3).required(),
}

//-----------------------------------------------------------------------------------------
// Model
const ItemsModel = db.define("items", {
	name: {
		type: Sequelize.STRING,
		field: "name"
	},
	description: {
		type: Sequelize.TEXT,
		field: "description"
	},
	rating: {
		type: Sequelize.DECIMAL,
		field: "rating"
	},
	category_id: {
		type: Sequelize.INTEGER,
		field: "category_id"
	},
	provider: {
		type: Sequelize.STRING,
		field: "provider"
	},
	price: {
		type: Sequelize.DECIMAL,
		field: "price"
	},
	image: {
		type: Sequelize.STRING,
		field: "image"
	},
	url: {
		type: Sequelize.STRING,
		field: "url"
	}
}, {timestamps: true})

const CatModel = db.define("categories", {
	category_name: {
		type: Sequelize.STRING,
		field: "category_name"
	}
})

ItemsModel.belongsTo(CatModel, {foreignKey: "category_id"})

//-----------------------------------------------------------------------------------------
// Routes
app.use("/api/images", express.static('uploads'))

app.get("/api/items", function(req, res){
    const data = req.query
    let min_price = data.min || 0
    let max_price = data.max || 100
    let categories = data.cat || [1]

    ItemsModel.findAll({
    	limit: 100,
    	include: [
    		{
    			model: CatModel,
    			attributes: ["category_name"]
    		}
    	],
    	where: {
    		category_id: categories,
    		price: {
    			[Op.and]: {
    				[Op.gte]: min_price,
    				[Op.lte]: max_price
    			}
    		}
    	},
    	attributes: ["name", "description", "rating", "provider", "price", "image", "url"],
    	raw: true
    })
		.then((result) => res.status(200).send(result))
		.catch((err) => res.status(400).send("Error found: " + err.errors[0].message))
})

app.get("/api/categories", function(req, res){
	CatModel.findAll({
		limit: 100,
		attributes: ["id", "category_name"]
	})
		.then((result) => res.status(200).send(result))
		.catch((err) => res.status(400).send("Error found: " + err.errors[0].message))
})

app.post("/api/items", function(req, res){
	const data = req.body
	data.image = "/api/images/" + data.image
	const test_res = Joi.validate(data, schema)
	if (test_res.error) {
		res.status(400).send("Error found: " + test_res.error.details[0].message)
	} else {
		ItemsModel.create(data)
			.then((result) => res.status(200).send("Successfully added item: " + data.name))
			.catch((err) => res.status(400).send("Error found: " + err.errors[0].message))
	}
})

app.post("/api/items/images/:filename", function(req, res){
	upload(req, res, function(err) {
		if(err) {
			res.status(400).send("Error found: " + err)
		} else {
			res.status(200).send("Successfully uploaded")
		}
	})
})

//-----------------------------------------------------------------------------------------
// Start App
app.listen(port, () => console.log(`
    ====================================
    SERVER STARTED AT: ${host}:${port}
    API created for HackNRoll 2019
    ====================================
`))