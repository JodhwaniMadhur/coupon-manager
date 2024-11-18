
<div align="center">

  <img src="https://github.com/Louis3797/awesome-readme-template/blob/main/assets/logo.png" alt="logo" width="200" height="auto" />
  <h1>Coupon Management API</h1>
  
  
  
  
<!-- Badges -->
<p>
  <a href="https://github.com/JodhwaniMadhur/coupon-manager/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/JodhwaniMadhur/coupon-manager" alt="contributors" />
  </a>
  <a href="">
    <img src="https://img.shields.io/github/last-commit/JodhwaniMadhur/coupon-manager" alt="last update" />
  </a>
  <a href="https://github.com/JodhwaniMadhur/coupon-manager/network/members">
    <img src="https://img.shields.io/github/forks/JodhwaniMadhur/coupon-manager" alt="forks" />
  </a>
  <a href="https://github.com/JodhwaniMadhur/coupon-manager/stargazers">
    <img src="https://img.shields.io/github/stars/JodhwaniMadhur/coupon-manager" alt="stars" />
  </a>
  <a href="https://github.com/JodhwaniMadhur/coupon-manager/issues/">
    <img src="https://img.shields.io/github/issues/JodhwaniMadhur/coupon-manager" alt="open issues" />
  </a>
  <a href="https://github.com/JodhwaniMadhur/coupon-manager/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/JodhwaniMadhur/coupon-manager.svg" alt="license" />
  </a>
</p>
   
<h4>
    <a href="https://github.com/JodhwaniMadhur/coupon-manager/">View Demo</a>
  <span> · </span>
    <a href="https://github.com/JodhwaniMadhur/coupon-manager">Documentation</a>
  <span> · </span>
    <a href="https://github.com/JodhwaniMadhur/coupon-manager/issues/">Report Bug</a>
  <span> · </span>
    <a href="https://github.com/JodhwaniMadhur/coupon-manager/issues/">Request Feature</a>
  </h4>
</div>

<br />

<!-- Table of Contents -->
# :notebook_with_decorative_cover: Table of Contents

- [About the Project](#star2-about-the-project)
  * [Tech Stack](#space_invader-tech-stack)
  * [Features](#dart-features)
  * [Environment Variables](#key-environment-variables)
- [Getting Started](#toolbox-getting-started)
  * [Prerequisites](#bangbang-prerequisites)
  * [Installation](#gear-installation)
  * [Running Tests](#test_tube-running-tests)
  * [Run Locally](#running-run-locally)
- [Usage](#eyes-usage)
- [Roadmap](#compass-roadmap)
- [Contributing](#wave-contributing)

  

<!-- About the Project -->
## :star2: This is a project for Coupon Management API. 
Coupons can be added, deleted as well as it can be validated against a cart.
Coupons can also be applied on a cart and then the API calculates the final amount of the cart after applicable coupon is applied



<!-- TechStack -->
### :space_invader: Tech Stack

<details>
  <summary>Client</summary>
  <ul>
    <li><a href="">Python</a></li>
  </ul>
</details>

<details>
  <summary>Server</summary>
  <ul>
    <li><a href="">Flask</a></li>
    
  </ul>
</details>

<details>
<summary>Database</summary>
  <ul>
    <li><a href="">MySQL</a></li>
  </ul>
</details>

<!-- Features -->
### :dart: Features

- Create Coupon [POST]
- Display All Coupons [GET]
- Get Coupon by Code [GET]
- Update Coupon [PUT]
- Delete Coupon [DELETE]
- Get Applicable Coupon [POST]
- Apply Coupon [POST]
- Health Check [GET]


<!-- Env Variables -->
### :key: Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`DATABASE_URL`

`SECRET_KEY` [Optional]

<!-- Getting Started -->
## 	:toolbox: Getting Started

<!-- Prerequisites -->
### :bangbang: Prerequisites

This project uses pip as package manager. Downlaod the get-pip.py from https://bootstrap.pypa.io/get-pip.py

```bash
 python get-pip.py
```

<!-- Installation -->
### :gear: Installation

Download my-project with git

```bash
  git clone https://github.com/JodhwaniMadhur/coupon-manager.git
  cd coupon-manager
```
   
<!-- Running Tests -->
### :test_tube: Running Tests

To run tests, run the following command

```bash
  
```

<!-- Run Locally -->
### :running: Run Locally

Clone the project

```bash
  git clone https://github.com/JodhwaniMadhur/coupon-manager.git
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  flask --app app run
```


<!-- Usage -->
## :eyes: Usage


1. Add a coupon:
API Type: POST
route: /api/coupons
return value: 200 response code.
considered coupon to be an alphanumeric string of length 10. this gives us 36^10 possibile codes, whereas if it was only number, the limit was the max int limit that an SQL column can take which is just 2,147,483,647.
```json
//Sample 1 cart wise coupon
{
    "code":"XYZ20",
    "type": "cart-wise",
    "description":"Get 20% off on whole order",
    "details": 
    {
        "threshold": 100,
        "discount": 20
    }
}

//Sample 2 product wise coupon
{
    "code":"MAGGI50",
    "type": "product-wise",
    "description":"Get 50% off on Maggi Products",
    "details": 
    {
        "product_id": 1,
        "discount": 50
    }
}

//RQ Sample 3 bxgy coupon
{
  "code": "BIGSALE",
  "description":"Buy 3 of X and Y each and get a Z free (Applicable twice)"
  "type": "bxgy",
  "details": {
    "buy_products": [
      {
        "product_id": 1,
        "quantity": 3
      },
      {
        "product_id": 2,
        "quantity": 3
      }
    ],
    "get_products": [
      {
        "product_id": 3,
        "quantity": 1
      }
    ],
    "repition_limit": 2
  }
}

```

2. Get all coupons:
API Type: GET
route: /api/coupons
Return Value: all couponsfrom the DB in json format.
Return all coupons saved in the DB

```json
//RS 
[
    {
        "code": "90OFF",
        "created_at": "2024-11-17T18:35:03",
        "description": "Save 90% on whole cart",
        "details": {
            "discount": 90,
            "threshold": 100
        },
        "expires_at": null,
        "is_active": true,
        "type": "cart-wise"
    },
    {
        "code": "MAGGI20",
        "created_at": "2024-11-17T18:36:36",
        "description": "Save 20% on all Maggi Products",
        "details": {
            "discount": 20,
            "product_id": 1
        },
        "expires_at": null,
        "is_active": true,
        "type": "product-wise"
    },
    {
        "code": "SAVEBIG",
        "created_at": "2024-11-17T18:33:25",
        "description": "Buy 3 products of X and Y and get a Z free(Applicable Twice)",
        "details": {
            "buy_products": [
                {
                    "product_id": 1,
                    "quantity": 3
                },
                {
                    "product_id": 2,
                    "quantity": 3
                }
            ],
            "get_products": [
                {
                    "product_id": 3,
                    "quantity": 1
                }
            ],
            "repition_limit": 2
        },
        "expires_at": null,
        "is_active": true,
        "type": "bxgy"
    }
]
```

3. Get a specifc coupon
API Type - GET
route - /api/coupons/coupon_code_here
```json
//JSON Response 
{
    "code": "90OFF",
    "created_at": "2024-11-17T18:35:03",
    "description": "Save 90% on whole cart",
    "details": {
        "discount": 90,
        "threshold": 100
    },
    "expires_at": null,
    "is_active": true,
    "type": "cart-wise"
}
```

4. Update Coupon
API Type: PUT
route: /api/coupons/<coupon_code>
Request Body: (Partial update supported)

```json
{
    "description": "Updated coupon description",
    "details": {
        "threshold": 200,
        "discount": 25
    },
    "is_active": false
}
```
Return Value: Updated coupon object
```json
{
    "code": "XYZ20",
    "created_at": "2024-11-17T18:35:03",
    "description": "Updated coupon description",
    "details": {
        "threshold": 200,
        "discount": 25
    },
    "expires_at": null,
    "is_active": false,
    "type": "cart-wise"
}
```

5. Get Applicable Coupons
API Type: POST
route: /api/applicable-coupons
Request Body:

```json
{
    "cart": { 
        "items": [ 
            {"product_id": 1, "quantity": 6, "price": 50}, 
            {"product_id": 2, "quantity": 3, "price": 30}, 
            {"product_id": 3, "quantity": 2, "price": 25} 
        ] 
    }
}
```
Return Value: JSON array of applicable coupons with their codes, types, and potential discounts
```json
{
    "applicable_coupons": [
        {
            "coupon_code": "XYZ20",
            "type": "cart-wise",
            "discount": 60
        },
        {
            "coupon_code": "MAGGI50",
            "type": "product-wise",
            "discount": 150
        }
    ]
}
```

6. Apply Coupon
API Type: POST
route: /api/apply-coupon/<coupon_code>
Request Body:

```json
{
    "cart": { 
        "items": [ 
            {"product_id": 1, "quantity": 6, "price": 50}, 
            {"product_id": 2, "quantity": 3, "price": 30}, 
            {"product_id": 3, "quantity": 2, "price": 25} 
        ] 
    }
}
```
Return Value: Updated cart with applied discount
```json
{
    "updated_cart": {
        "items": [ ... ],
        "total_before_discount": 500,
        "total_discount": 100,
        "total_after_discount": 400
    }
}
```

<!-- Roadmap -->
## :compass: Roadmap

* [ ] Add Multi coupon support


<!-- Contributing -->
## :wave: Contributing

<a href="https://github.com/JodhwaniMadhur/coupon-manager/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=JodhwaniMadhur/coupon-manager" />
</a>


Contributions are always welcome!


<!-- FAQ -->
## :grey_question: FAQ

What types of coupons are supported?

The API supports three types of coupons:

Cart-wise: Discount applied to the entire cart when a minimum threshold is met
Product-wise: Discount applied to specific products
Buy X Get Y (BXGY): Buy a certain quantity of products and get another product free




How are coupon codes generated?

Coupon codes are alphanumeric strings of length 10
This approach provides approximately 36^10 possible unique codes
Significantly larger than traditional numeric coupon codes


Can a coupon be applied multiple times?

For BXGY type coupons, a repition_limit can be set to control how many times the coupon can be applied
Other coupon types typically have their own validation rules in the CouponService


How does the system handle coupon validation?

Coupons are validated based on:

Coupon active status
Matching product requirements
Minimum cart value thresholds
Quantity-based conditions for BXGY coupons




What happens if a coupon is not applicable?

The /applicable-coupons endpoint will simply not include non-applicable coupons
When trying to apply an invalid coupon, a specific CouponError will be raised


Can I update an existing coupon?

Yes, you can use the PUT method on /coupons/<coupon_code> to update coupon details
Partial updates are supported, meaning you don't need to provide all fields


How are database errors handled?

The API includes specific error handlers for:

Validation errors
Database errors
Coupon-specific errors


Errors are logged and returned with appropriate HTTP status codes


Is there a way to check the API's health?

Yes, use the /health endpoint to:

Check database connectivity
Verify API responsiveness
Get current timestamp




What are the future plans for this API?

The roadmap mentions adding multi-coupon support
Potential improvements could include more complex discount rules, expiration handling, and enhanced reporting


How are coupons stored?

Coupons are stored in a MySQL database
Each coupon has fields like code, type, description, details, creation time, and active status


Are there any limitations on coupon creation?

Coupon codes must be unique
The system prevents creating a coupon with an existing code
Detailed validation is performed using Marshmallow schemas


<!-- License -->
## :warning: License

Distributed under the no License. See LICENSE.txt for more information.
