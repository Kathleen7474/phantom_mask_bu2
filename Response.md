---
title: Response

---

# Response

> Note: This API documentation **assumes that the frontend already has access to valid pharmacy_id and user_id values.** These IDs are used in various endpoint paths and request parameters.
## API Document
* [x] List pharmacies, optionally filtered by specific time and/or day of the week.
    * Implemented at GET /pharmacies and POST /pharmacies 
    * Query Parameters:
        • day (optional): Day of the week (e.g., Mon, Tue, Wed, Thur, Fri, Sat, Sun)
        • time (optional): Specific time in HH:MM 24-hour format (e.g., 15:30)
    * Response Format: The API returns a list of pharmacies. Each pharmacy object contains:
    •	id (integer): Unique pharmacy identifier
    •	name (string): Name of the pharmacy
    •	openingHours (array): List of opening time entries for each day the pharmacy operates
    • Each entry includes:
        -   day (string): Day of the week (e.g., "Mon", "Tue", etc.)
        - open (string): Opening time in HH:MM 24-hour format
        - close (string): Closing time in HH:MM 24-hour format
    * Supports the following example cases (not limited to these):
        - (Response 1) GET /pharmacies: list all pharmacies
        - (Response 2) GET /pharmacies?day=Thu: list pharmacies that are open on Thursday
        - (Response 3) GET /pharmacies?day=Thu&time=15:30: list pharmacies that are open at 15:30 on Thursday
        - (Response 4 & 5) If the time format is invalid (e.g., time=99:99 or day="Man"), the API returns a 400 Bad Request
    * Note: In the provided JSON data file, some pharmacies operate overnight. Therefore, I split the overnight opening hours into two separate entries.
For example, instead of "Mon: 18:00 to 05:00", it is represented as:
"Mon: 18:00 to 23:59" and "Tue: 00:00 to 05:00"

<details>
  <summary>Response 1 json</summary>
  <pre><code class="language-json">
HTTP Status Code: 200 OK
[
    {
        "id": 1,
        "name": "DFW Wellness",
        "openingHours": [
            {
                "close": "18:00",
                "day": "Mon",
                "open": "08:00"
            },
            {
                "close": "18:00",
                "day": "Tue",
                "open": "13:00"
            }
            //...
        ]
    },
    {
        "id": 2,
        "name": "Carepoint",
        "openingHours": [
            {
                "close": "21:00",
                "day": "Mon",
                "open": "08:00"
            }
            //...
        ]
    }
    //...
]  
  </code></pre>
</details>

<details>
  <summary>Response 2 json (response all available pharmacies on Thursday)</summary>
  <pre><code class="language-json">
HTTP Status Code: 200 OK
[
    {
        "id": 1,
        "name": "DFW Wellness",
        "openingHours": [
            {
                "close": "18:00",
                "day": "Mon",
                "open": "08:00"
            },
            {
                "close": "18:00",
                "day": "Tue",
                "open": "13:00"
            },
            {
                "close": "18:00",
                "day": "Wed",
                "open": "08:00"
            },
            {
                "close": "18:00",
                "day": "Thur",
                "open": "13:00"
            },
            {
                "close": "18:00",
                "day": "Fri",
                "open": "08:00"
            }
        ]
    },
    {
        "id": 2,
        "name": "Carepoint",
        "openingHours": [
            {
                "close": "21:00",
                "day": "Mon",
                "open": "08:00"
            },
            {
                "close": "21:00",
                "day": "Tue",
                "open": "08:00"
            },
            {
                "close": "21:00",
                "day": "Wed",
                "open": "08:00"
            },
            {
                "close": "21:00",
                "day": "Thur",
                "open": "08:00"
            },
            {
                "close": "21:00",
                "day": "Fri",
                "open": "08:00"
            }
        ]
    }
    //...
]
  </code></pre>
</details>

<details>
  <summary>Response 3 json (response all available pharmacies at 15:30 on Thursday)</summary>
  <pre><code class="language-json">
HTTP Status Code: 200 OK
[
    {
        "id": 3,
        "name": "First Care Rx",
        "openingHours": [
            {
                "close": "23:59",
                "day": "Mon",
                "open": "08:00"
            },
            {
                "close": "17:00",
                "day": "Tue",
                "open": "00:00"
            },
            {
                "close": "23:59",
                "day": "Wed",
                "open": "08:00"
            },
            {
                "close": "17:00",
                "day": "Thur",
                "open": "00:00"
            },
            {
                "close": "23:59",
                "day": "Fri",
                "open": "08:00"
            }
        ]
    },
    {
        "id": 16,
        "name": "RX Universal",
        "openingHours": [
            {
                "close": "23:59",
                "day": "Mon",
                "open": "23:00"
            },
            {
                "close": "12:00",
                "day": "Tue",
                "open": "00:00"
            },
            {
                "close": "23:59",
                "day": "Tue",
                "open": "23:00"
            },
            {
                "close": "12:00",
                "day": "Wed",
                "open": "00:00"
            },
            {
                "close": "23:59",
                "day": "Wed",
                "open": "23:00"
            },
            {
                "close": "12:00",
                "day": "Thur",
                "open": "00:00"
            },
            {
                "close": "23:59",
                "day": "Thur",
                "open": "23:00"
            },
            {
                "close": "12:00",
                "day": "Fri",
                "open": "00:00"
            },
            {
                "close": "23:59",
                "day": "Fri",
                "open": "23:00"
            },
            {
                "close": "12:00",
                "day": "Sat",
                "open": "00:00"
            }
        ]
    }
    //...
]
  </code></pre>
</details>
<details>
  <summary>Response 4 json (invalid day)</summary>
  <pre><code class="language-json">
HTTP Status Code: 400 Bad Request
{
    "error": "Invalid day parameter. Allowed values: ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']"
}
  </code></pre>
</details>
<details>
  <summary>Response 5 json (invalid time)</summary>
  <pre><code class="language-json">
HTTP Status Code: 400 Bad Request
{
    "error": "Invalid time format, expected HH:MM"
}
  </code></pre>
</details>


* [x] List all masks sold by a given pharmacy with an option to sort by name or price.
    * Implemented at GET /pharmacies/\<int:pharmacy_id>/masks or POST /pharmacies/\<int:pharmacy_id>/masks 
    * Path Paramters:
        * pharmacy_id (interger): ID of the pharmacy
    * Query Parameters:
        • sort_by (optional): Sorting criteria, either name or price
    * Response Format: The API returns a json object contains:
        •	pharmacy (string): the name of the pharmacy
        •   masks (array): List of mask objects sold by the pharmacy. 
        •   Each mask object includes:
       - id (integer): Unique mask identifier
       - name (string): Name of the mask product
       - price (float): Price of the mask
       - stockQuantity (float): Current stock quantity of the mask
    * Supports the following example cases (not limited to these):
        1.	(Response 1) GET /pharmacies/3/masks: list all the mask sold by pharmacy with ID 3. If the `sort_by` parameter is missing or invalid (e.g., `sort_by=abc`), the default unsorted result will be returned.
        2.	(Response 2) GET /pharmacies/3/masks?sort_by=name: list all the mask sold by a given pharmacy sort by name
        3.	(Response 3) GET /pharmacies/3/masks?sort_by=price: list all the mask sold by a given pharmacy sort by price
        4.	(404 NOT FOUND) If pharmacy_id does not exist, API returns a 404 Not Found error.
<details>
  <summary>Response 1 json (unsorted)</summary>
  <pre><code class="language-json">
HTTP Status Code: 200 OK
{
    "masks": [
        {
            "id": 7,
            "name": "Second Smile (blue) (10 per pack)",
            "price": 49.83,
            "stockQuantity": 12.0
        },
        {
            "id": 8,
            "name": "Second Smile (green) (6 per pack)",
            "price": 27.69,
            "stockQuantity": 12.0
        },
        {
            "id": 9,
            "name": "Second Smile (blue) (6 per pack)",
            "price": 11.07,
            "stockQuantity": 12.0
        }
        //...
    ],
    "pharmacy": "First Care Rx"
}
  </code></pre>
</details>
<details>
  <summary>Response 2 json (sort by name)</summary>
  <pre><code class="language-json">
HTTP Status Code: 200 OK
{
    "masks": [
        {
            "id": 13,
            "name": "MaskT (black) (10 per pack)",
            "price": 44.4,
            "stockQuantity": 11.0
        },
        {
            "id": 14,
            "name": "MaskT (green) (10 per pack)",
            "price": 37.87,
            "stockQuantity": 11.0
        },
        {
            "id": 10,
            "name": "Masquerade (black) (10 per pack)",
            "price": 19.95,
            "stockQuantity": 12.0
        }
        //...
    ],
    "pharmacy": "First Care Rx"
}
  </code></pre>
</details>
<details>
  <summary>Response 3 json (sort by price)</summary>
  <pre><code class="language-json">
HTTP Status Code: 200 OK
{
    "masks": [
        {
            "id": 9,
            "name": "Second Smile (blue) (6 per pack)",
            "price": 11.07,
            "stockQuantity": 12.0
        },
        {
            "id": 12,
            "name": "Masquerade (black) (3 per pack)",
            "price": 12.0,
            "stockQuantity": 12.0
        },
        {
            "id": 15,
            "name": "Second Smile (black) (3 per pack)",
            "price": 14.96,
            "stockQuantity": 11.0
        }
        //...
    ],
    "pharmacy": "First Care Rx"
}
  </code></pre>
</details>


* [x] List all pharmacies that offer a number of mask products within a given price range, where the count is above, below, or between given thresholds.
  * Implemented at GET /pharmacies/mask_count_by_price or POST /pharmacies/mask_count_by_price
  * Query Parameters:
	•	lower_price (optional, default: 0): Minimum price to filter mask products
	•	upper_price (optional, default: ∞): Maximum price to filter mask products
	•	threshold_lower (optional, default: 0): Lower bound for the number of matching mask products
	•	threshold_upper (optional, default: ∞): Upper bound for the number of matching mask products
  * Response Format: The API returns a dictionary with three categories:
      •	below: pharmacies with fewer than threshold_lower matching masks
      •	between: pharmacies with mask count between threshold_lower and threshold_upper (inclusive)
      •	above: pharmacies with more than threshold_upper matching masks
      •	Each pharmacy object contains:
      - id (integer): Pharmacy ID
      - name (string): Pharmacy name
      - matchingMaskCount (integer): Number of masks within the specified price range
      - matchingMasks (array): List of mask objects
      - Each mask object contains:
	•	id (integer): Mask ID
	•	name (string): Mask name
	•	price (float): Mask price
  * Supports the following example cases (not limited to these):
     1.	(Response 1) GET /pharmacies/mask_count_by_price?lower_price=10&upper_price=20&threshold_lower=2&threshold_upper=3: List all pharmacies where the number of masks priced between 10 and 20 is below 2, between 2 and 3 (inclusive), or above 3.
     2.	(Response 2 & 3) If upper_price is less than lower_price, or threshold_upper is less than threshold_lower, the API returns a 400 Bad Request.
     3.	(Response 4)  If any of the input values such as lower_price, upper_price, threshold_lower, or threshold_upper are invalid (e.g., non-numeric or incorrectly formatted), the API returns a 400 Bad Request.

<details>
  <summary>Response 1 json</summary>
  <pre><code class="language-json">
HTTP Status Code: 200 OK
{
    "above": [
        {
            "id": 3,
            "matchingMaskCount": 4,
            "matchingMasks": [
                {
                    "id": 9,
                    "name": "Second Smile (blue) (6 per pack)",
                    "price": 11.07
                },
                {
                    "id": 10,
                    "name": "Masquerade (black) (10 per pack)",
                    "price": 19.95
                },
                {
                    "id": 12,
                    "name": "Masquerade (black) (3 per pack)",
                    "price": 12.0
                },
                {
                    "id": 15,
                    "name": "Second Smile (black) (3 per pack)",
                    "price": 14.96
                }
            ],
            "name": "First Care Rx"
        }
        //...
    ],
    "below": [
        {
            "id": 1,
            "matchingMaskCount": 1,
            "matchingMasks": [
                {
                    "id": 1,
                    "name": "True Barrier (green) (3 per pack)",
                    "price": 13.7
                }
            ],
            "name": "DFW Wellness"
        }
        //...
    ],
    "between": [
        {
            "id": 10,
            "matchingMaskCount": 2,
            "matchingMasks": [
                {
                    "id": 42,
                    "name": "Masquerade (black) (6 per pack)",
                    "price": 12.05
                },
                {
                    "id": 44,
                    "name": "Masquerade (blue) (6 per pack)",
                    "price": 12.9
                }
            ],
            "name": "Below Drug"
        }
        //...
    ]
}
  </code></pre>
</details>


<details>
  <summary>Response 2 json (upper_price is less than lower_price)</summary>
  <pre><code class="language-json">
HTTP Status Code:  400 BAD REQUEST
{
    "error": "upper_price must be greater than or equal to lower_price"
}
  </code></pre>
</details>
<details>
  <summary>Response 2 json (threshold_upper is less than threshold_lower)</summary>
  <pre><code class="language-json">
HTTP Status Code:  400 BAD REQUEST
{
    "error": "threshold_upper must be greater than or equal to threshold_lower"
}
  </code></pre>
</details>
<details>
  <summary>Response 4 json (invalid input)</summary>
  <pre><code class="language-json">
HTTP Status Code:  400 BAD REQUEST
{
    "error": "Invalid query parameters"
}
  </code></pre>
</details>

* [x] Show the top N users who spent the most on masks during a specific date range.
  * Implemented at GET /users/top-spenders or POST /users/top-spenders
  * Query Parameters:
	•	start (optional): Start date (inclusive) in YYYY-MM-DD format (e.g., 2024-01-01)
    •	end (optional): End date (inclusive) in YYYY-MM-DD format (e.g., 2024-12-31)
	•	n (optional): Number of top spenders to return (default: 5)
  * Response Format: The API returns a list of top N spenders (ordered by total spending in descending order). Each entry includes:
  • id (int): User id
  • name (string): Name of the user
  • total_spending (float): Total spending amount 
  * Supports the following example cases (not limited to these):
    1.	(Response 1) GET /users/top-spenders: list top 5 spenders of all time (default N=5)
	2.	(Response 2) GET /users/top-spenders?start=2024-01-01&n=3: list top 3 spenders since 2024-01-01
	3.	(Response 3) GET /users/top-spenders?start=2025-01-01&end=2025-06-12&n=3: list top 3 spenders from 2025-01-01 to 2025-06-12
	4.	(Response 4 & 5)  If the start or end parameters are not in the correct YYYY-MM-DD format, or if n is not a valid integer (e.g., n=abc), the API returns a 400 Bad Request.


<details>
  <summary>Response 1 json (top 5 spenders of all time)</summary>
  <pre><code class="language-json">
HTTP Status Code: 200 OK
[
    {
        "id": 1,
        "name": "Yvonne Guerrero",
        "total_spending": 183.91
    },
    {
        "id": 3,
        "name": "Geneva Floyd",
        "total_spending": 180.41
    },
    {
        "id": 8,
        "name": "Timothy Schultz",
        "total_spending": 170.56
    },
    {
        "id": 4,
        "name": "Lester Arnold",
        "total_spending": 165.16
    },
    {
        "id": 2,
        "name": "Ada Larson",
        "total_spending": 163.82
    }
]
  </code></pre>
</details>

<details>
  <summary>Response 2 json (top 3 spenders since 2024-01-01)</summary>
  <pre><code class="language-json">
HTTP Status Code: 200 OK
[
    {
        "id": 1,
        "name": "Yvonne Guerrero",
        "total_spending": 183.91
    },
    {
        "id": 3,
        "name": "Geneva Floyd",
        "total_spending": 180.41
    },
    {
        "id": 8,
        "name": "Timothy Schultz",
        "total_spending": 170.56
    }
]
  </code></pre>
</details>
<details>
  <summary>Response 3 json (top 3 spenders from 2025-01-01 to 2025-06-12)</summary>
  <pre><code class="language-json">
HTTP Status Code: 200 OK
[
    {
        "id": 1,
        "name": "Yvonne Guerrero",
        "total_spending": 172.05
    },
    {
        "id": 4,
        "name": "Lester Arnold",
        "total_spending": 160.17
    },
    {
        "id": 8,
        "name": "Timothy Schultz",
        "total_spending": 155.41
    }
]
  </code></pre>
</details>
<details>
  <summary>Response 4 json (date time)</summary>
  <pre><code class="language-json">
HTTP Status Code:  400 BAD REQUEST
{
    "error": "Invalid date format. Use YYYY-MM-DD"
}
  </code></pre>
</details>
<details>
  <summary>Response 5 json (invalid "n")</summary>
  <pre><code class="language-json">
HTTP Status Code:  400 BAD REQUEST
{
    "error": "Invalid 'n' parameter. Must be an integer."
}
  </code></pre>
</details>

* [x] Process a purchase where a user buys masks from multiple pharmacies at once.
  *  Implemented at POST /users/<int:user_id>/purchase
  *  Path Parameter: 
      *  user_id (integer): ID of the user making the purchase
  *  Request Body (JSON):
      *  items (array): A list of purchase items. Each item should contain:
	•	pharmacy_id (integer): ID of the pharmacy
	•	mask_name (string): Name of the mask
	•	quantity (integer): Quantity to purchase
    * Response Format:
        * message (string): Confirmation message of the purchase result
        * total_spent (float): Total amount spent in this transaction
        * remaining_balance (float): The user's updated cash balance after the purchase
    * Note: The purchase time is based on the timestamp when the request is received, which is used to **determine whether the pharmacy is currently open**.
    * Supports the following example cases (not limited to these):
        * (Request and Response 1) POST **/users/3/purchase** with valid items: Complete the purchase and return total spent and remaining balance.
        * (415 UNSUPPORTED MEDIA TYPE) If the request body is missing or is not JSON
        * (Request and Response 2) If items is missing from the request body, return 400 Bad Request with a message: "Missing purchase items".
        * (Request and Response 3 & 4) If any pharmacy_id is missing or not found, return:
            * 400 Bad Request for missing pharmacy_id
            * 404 Not Found if the pharmacy does not exist
        * (Request and Response 5) If the pharmacy is closed at the current time, return 400 Bad Request with the current time and error message.
        * (Request and Response 6 & 7) If mask_name is missing, or the mask does not exist in the given pharmacy, return:
            *  400 Bad Request for missing mask_name
            *  404 Not Found if the mask does not exist
        * (Request and Response 8) If quantity is invalid (non-integer or <= 0), return 400 Bad Request.
        * (Request and Response 9) If the mask stock is insufficient, return 400 Bad Request.
        * (Request and Response 10) If the user does not have enough balance, return 400 Bad Request.

<details>
  <summary>Request and Response 1</summary>
  <pre><code class="language-json">
Request 1{
  "items": [
    {
      "pharmacy_id": 19,
      "mask_name": "True Barrier (green) (10 per pack)",
      "quantity": 2
    },
    {
      "pharmacy_id": 2,
      "mask_name": "Masquerade (blue) (6 per pack)",
      "quantity": 1
    }
  ]
}

 </code></pre>
<pre><code class="language-json">
Response 1:  HTTP Status Code:  200 OK  
{
    "message": "Purchase completed successfully",
    "remaining_balance": 7.43,
    "total_spent": 54.33
}
  </code></pre>
</details>
<details>
  <summary>Request and Response 2 ("item" missing)</summary>
  <pre><code class="language-json">
Request 2{
}
 </code></pre>
<pre><code class="language-json">
Response 2: HTTP Status Code:  400 BAD REQUEST
{
    "error": "Missing purchase items"
}
  </code></pre>
</details>
<details>
  <summary>Request and Response 3 ("pharmacy id" missing)</summary>
  <pre><code class="language-json">
Request 3{
  "items": [
    {
      "mask_name": "True Barrier (green) (10 per pack)",
      "quantity": 2
    }
  ]
}
 </code></pre>
<pre><code class="language-json">
Response 3: HTTP Status Code:  400 BAD REQUEST
{
    "error": "Missing pharmacy_id in an item"
}
  </code></pre>
</details>
<details>
  <summary>Request and Response 4 ("pharmacy id" not found)</summary>
  <pre><code class="language-json">
Request 4{
  "items": [
    {
      "pharmacy_id": 200,
      "mask_name": "True Barrier (green) (10 per pack)",
      "quantity": 2
    }
  ]
}
 </code></pre>
<pre><code class="language-json">
Response 4: HTTP Status Code:  404 NOT FOUND
{
    "error": "Pharmacy with id '200' not found"
}
  </code></pre>
</details>

<details>
  <summary>Request and Response 5 (pharmacy not open)</summary>
  <pre><code class="language-json">
Request 5{
  "items": [
    {
      "pharmacy_id": 1,
      "mask_name": "True Barrier (green) (10 per pack)",
      "quantity": 2
    },
    {
      "pharmacy_id": 2,
      "mask_name": "Masquerade (blue) (6 per pack)",
      "quantity": 1
    }
  ]
}
 </code></pre>
<pre><code class="language-json">
Response 5: HTTP Status Code:  400 BAD REQUEST
{
    "error": "Pharmacy 'DFW Wellness' is currently closed (now: Wed 18:50)"
}
  </code></pre>
</details>

<details>
  <summary>Request and Response 6 ("mask name" missing)</summary>
  <pre><code class="language-json">
Request 6{
  "items": [
    {
      "pharmacy_id": 1,
      "quantity": 2
    }
  ]
}
 </code></pre>
<pre><code class="language-json">
Response 6: HTTP Status Code:  400 BAD REQUEST
{
    "error": "Missing mask_name in an item"
}
  </code></pre>
</details>

<details>
  <summary>Request and Response 7 ("mask name" not found)</summary>
  <pre><code class="language-json">
Request 7{
  "items": [
    {
      "pharmacy_id": 19,
      "mask_name": "Apples (green) (10 per pack)",
      "quantity": 2
    }
   
  ]
}
 </code></pre>
<pre><code class="language-json">
Response 7: HTTP Status Code:  404 NOT FOUND
{
    "error": "Mask 'Apples (green) (10 per pack)' not found in pharmacy id '19'"
}
  </code></pre>
</details>

<details>
  <summary>Request and Response 8 (quantity invalid)</summary>
  <pre><code class="language-json">
Request 8{
  "items": [
    {
      "pharmacy_id": 19,
      "mask_name": "Cotton Kiss (blue) (10 per pack)",
      "quantity": "abc"
    }
  ]
}
 </code></pre>
<pre><code class="language-json">
Response 8: HTTP Status Code:  400 BAD REQUEST
{
    "error": "Invalid quantity for 'Cotton Kiss (blue) (10 per pack)'"
}
  </code></pre>
</details>

<details>
  <summary>Request and Response 9 (stock insufiicient)</summary>
  <pre><code class="language-json">
Request 9{
  "items": [
    {
      "pharmacy_id": 19,
      "mask_name": "Cotton Kiss (blue) (10 per pack)",
      "quantity": 200
    },
    {
      "pharmacy_id": 2,
      "mask_name": "Masquerade (blue) (6 per pack)",
      "quantity": 1
    }
  ]
}
 </code></pre>
<pre><code class="language-json">
Response 9: HTTP Status Code:  400 BAD REQUEST
{
    "error": "Not enough stock for 'Cotton Kiss (blue) (10 per pack)' in pharmacy id '19'"
}
  </code></pre>
</details>

<details>
  <summary>Request and Response 10 (user doesn't have enough balance)</summary>
  <pre><code class="language-json">
Request 10{
  "items": [
    {
      "pharmacy_id": 19,
      "mask_name": "Cotton Kiss (blue) (10 per pack)",
      "quantity": 1
    },
    {
      "pharmacy_id": 2,
      "mask_name": "Masquerade (blue) (6 per pack)",
      "quantity": 1
    }
  ]
}
 </code></pre>
<pre><code class="language-json">
Response 10: HTTP Status Code:  400 BAD REQUEST
{
    "error": "User does not have enough balance"
}
  </code></pre>
</details>

* [x] Update the stock quantity of an existing mask product by increasing or decreasing it.
  * Implemented at POST /pharmacies/\<int:pharmacy_id>/masks/adjust
  *  Path Parameter: 
      *  pharmacy_id (integer): The ID of the pharmacy where the mask stock should be adjusted.
  *  Request Body (JSON):
      *  mask_name (string): The name of the mask product to be adjusted.
      *  adjustment (integer): A positive or negative value indicating how much to increase or decrease the stock.
      *  
    * Response Format:
        * message (string): Confirmation message for stocj update
        * mask_name (string): Name of the updated mask product.
        * new_stock_quantity (number): The new stock quantity after adjustment.
    * Supports the following example cases (not limited to these):
        * (Request and Response 1) POST **/pharmacies/2/masks/adjust** with valid mask_name and adjustment: Update stock and return new quantity.
        * (Request and Response 2) If mask_name or adjustment is missing from the request body, return 400 Bad Request.
        * (Response 3) If adjustment is not a valid number, return 400 Bad Request.
        * (Response 4) If the mask does not exist in the given pharmacy, return 404 Not Found.
        * (Response 5) If the resulting stock would be negative, return 400 Bad Request.

<details>
  <summary>Request and Response 1</summary>
  <pre><code class="language-json">
Request 1{
  "mask_name": "Masquerade (blue) (6 per pack)",
  "adjustment": 5
}
 </code></pre>
<pre><code class="language-json">
Response 1: HTTP Status Code:  200 OK
{
    "mask_name": "Masquerade (blue) (6 per pack)",
    "message": "Stock updated successfully",
    "new_stock_quantity": 5.0
}
  </code></pre>
</details>

<details>
  <summary>Request and Response 2 ("mask_name" or "adjustmet" missing)</summary>
  <pre><code class="language-json">
Request 2{
  "adjustment": 5
}
 </code></pre>
<pre><code class="language-json">
Response 2: HTTP Status Code:  400 BAD REQUEST
{
    "error": "Missing 'mask_name' or 'adjustment' in request body"
}
  </code></pre>
</details>

<details>
  <summary>Request and Response 3 ("adjustmet" invalid)</summary>
  <pre><code class="language-json">
Request 2{
 "mask_name": "Masquerade (blue) (6 per pack)",
  "adjustment": "abc"
}
 </code></pre>
<pre><code class="language-json">
Response 3: HTTP Status Code:  400 BAD REQUEST
{
    "error": "'adjustment' must be a number"
}
  </code></pre>
</details>

<details>
  <summary>Request and Response 4 (mask not found)</summary>
  <pre><code class="language-json">
Request 4{
  "mask_name": "apples (6 per pack)",
  "adjustment": 5
}
 </code></pre>
<pre><code class="language-json">
Response 4: HTTP Status Code:  404 NOT FOUND
{
    "error": "Mask 'apples (6 per pack)' not found in pharmacy id 2"
}
  </code></pre>
</details>

<details>
  <summary>Request and Response 5 (negative stock)</summary>
  <pre><code class="language-json">
Request 5{
  "mask_name": "apples (6 per pack)",
  "adjustment": -100
}
 </code></pre>
<pre><code class="language-json">
Response 5: HTTP Status Code:  400 BAD REQUEST
{
    "error": "Stock quantity cannot be negative"
}
  </code></pre>
</details>

* [x] Create or update multiple mask products for a pharmacy at once, including name, price, and stock quantity.
  * Implemented at POST /pharmacies/\<int:pharmacy_id>/masks/batch
  * Path Parameters:
      - pharmacy_id (integer): ID of the pharmacy where the masks will be created or updated.
  * Request Body (JSON):
      * masks (array): A list of mask objects to be created or updated.Each mask object should contain:
        • name (string): Mask product name
        • price (float): Unit price of the mask
        • stock_quantity (integer): Number of masks in stock
  * Response Format:
      * results (array): Each entry includes:
         • mask (string): Mask name
         • status (string): Either "created", "updated", or "invalid input"
  * Supports the following example cases (not limited to these):
      * (Request and Response 1) POST **/pharmacies/3/masks/batch** with existing masks in list: Some masks are updated, new ones are created.
      * (Response 2) If 'masks' is missing from the request body, return 400 Bad Request.
      * (Response 3 & 4) If any mask object has missing or invalid fields (e.g., no name, price, or stock_quantity), that entry will be skipped with status "invalid input".
      * (404 NOT FOUND) POST /pharmacies/100/masks/batch If pharmacy_id does not exist, return 404 Not Found.

<details>
  <summary>Request and Response 1</summary>
  <pre><code class="language-json">
Request 1{
  "masks": [
    {
      "name": "Cute Masks (purple) (10 per pack)",
      "price": 25.5,
      "stock_quantity": 10
    },
    {
      "name": "True Barrier (black) (6 per pack)",
      "price": 12.3,
      "stock_quantity": 9
    }
  ]
}
 </code></pre>
<pre><code class="language-json">
Response 1: HTTP Status Code:  200 OK
{
    "results": [
        {
            "mask": "Cute Masks (purple) (10 per pack)",
            "status": "created"
        },
        {
            "mask": "True Barrier (black) (6 per pack)",
            "status": "updated"
        }
    ]
}
  </code></pre>
</details>

<details>
  <summary>Request and Response 2("masks" missing)</summary>
  <pre><code class="language-json">
Request 2{
  
}
 </code></pre>
<pre><code class="language-json">
Response 2: HTTP Status Code:  400 BAD REQUEST
{
    "error": "Missing 'masks' data"
}
  </code></pre>
</details>

<details>
  <summary>Request and Response 3("masks" name missing)</summary>
  <pre><code class="language-json">
Request 3{
  "masks": [
    {
      "price": 5,
      "stock_quantity": 10
    }
  ]
}
 </code></pre>
<pre><code class="language-json">
Response 3: HTTP Status Code:  400 BAD REQUEST
{
    "results": [
        {
            "mask": "(missing name)",
            "status": "invalid input"
        }
    ]
}
  </code></pre>
</details>

<details>
  <summary>Request and Response 4("masks" object error)</summary>
  <pre><code class="language-json">
Request 4{
  "masks": [
    {
      "name": "Cute Masks (purple) (10 per pack)",
      "price": 25.5,
      "stock_quantity": 10
    },
    {
      "name": "True Barrier (black) (6 per pack)",
      "price": "abnc",
      "stock_quantity": 9
    }
  ]
}
 </code></pre>
<pre><code class="language-json">
Response 4: HTTP Status Code:  400 BAD REQUEST
{
    "results": [
        {
            "mask": "Cute Masks (purple) (10 per pack)",
            "status": "updated"
        },
        {
            "mask": "True Barrier (black) (6 per pack)",
            "status": "invalid input"
        }
    ]
}
  </code></pre>
</details>



* [x] Search for pharmacies or masks by name and rank the results by relevance to the search term.
  * Implemented at GET /search
  * Query Parameters:
      * q (string, required): Search query string to match pharmacy or mask names.
      * limit (integer, optional, default=10): Maximum number of results to return.
  * Response Format:
    * An array of search result objects, each containing:
        • pharmacy (string): Name of the pharmacy
        • mask (string): Name of the mask product
        • price (float): Price of the mask
        • stock (integer): Available stock quantity
        • score (integer or float): Relevance score for the matched result
  * Response Format:
      * (Response 1) GET /search?q=Welltrack True Barrier black&limit=5 Search for "Welltrack True Barrier black" in pharmacy and mask names, return top 5 results by relevance score.
      * (Response 2) GET /search If the query parameter `q` is missing or empty, the API returns 400 Bad Request.
      * (Response 3) GET /search?q=Welltrack True Barrier black&limit=abc  If the `limit` parameter is not a valid integer, the API returns 400 Bad Request.

<details>
  <summary>Response 1 json</summary>
  <pre><code class="language-json">
HTTP Status Code: 200 OK
[
    {
        "mask": "True Barrier (green) (10 per pack)",
        "pharmacy": "Welltrack",
        "price": 20.58,
        "score": 21,
        "stock": 11.0
    },
    {
        "mask": "True Barrier (black) (6 per pack)",
        "pharmacy": "First Care Rx",
        "price": 12.3,
        "score": 16,
        "stock": 9.0
    },
    {
        "mask": "Cotton Kiss (black) (10 per pack)",
        "pharmacy": "Welltrack",
        "price": 16.31,
        "score": 16,
        "stock": 10.0
    },
    {
        "mask": "True Barrier (black) (10 per pack)",
        "pharmacy": "First Pharmacy",
        "price": 46.13,
        "score": 16,
        "stock": 12.0
    },
    {
        "mask": "True Barrier (black) (10 per pack)",
        "pharmacy": "Keystone Pharmacy",
        "price": 17.0,
        "score": 16,
        "stock": 12.0
    }
]
  </code></pre>
</details>
<details>
  <summary>Response 2 json ("q" missing)</summary>
  <pre><code class="language-json">
HTTP Status Code: 400 BAD REQUEST
{
    "error": "Search query is required"
}
  </code></pre>
</details>

<details>
  <summary>Response 3 json ("limit" invalid)</summary>
  <pre><code class="language-json">
HTTP Status Code: 400 BAD REQUEST
{
    "error": "Limit must be an integer"
}
  </code></pre>
</details>


## Import Data Commands
Please run the following command to initialize and migrate the data into the database:

```bash
$ python init_db.py
```
After running this command, a database file named phantom_mask.db will be created in the root directory of the project.


## Deployment

### Deploying on Render.com (Hosted Demo)

The project is currently deployed on Render.com. The API endpoints are available at the following URL for testing and development: https://phantom-mask-bu2.onrender.com

Note: Render’s free tier instances will automatically sleep after a period of (15 min) inactivity, the server is likely to be asleep when testing, which may cause the first request after idle to experience a delay of up to ~50 seconds.

### Running Locally

Please follow these steps to run the project locally
	1.	Environment Requirements: Python 3.x
	2.	Install dependencies:
```bash=
pip install -r requirements.txt
```
3. Set up the database: The existing SQLite database file in the project directory can be used directly. Alternatively, to create a new database with the required tables, please refer to the command mentioned earlier (Import Data Commands) to initialize it.
4. Run the application: 
```bash=
python main.py
```
5. Access the service: By default, Flask runs on port 5000. If this port conflicts with other services, the port number in main.py may need to be changed.
```python=
app.run(port=AVAILABLE_PORT)
```
    

## Additional Data

### ERD

### Folder Structure
```
root/
├── app/
│   ├── routes/
│   │   └── users.py
│   │   └── pharmacy.py
│   ├── utils/
│   │   └── load_users.py
│   │   └── load_pharmacies.py
│   │   └── search_utils.py
│   └── __init__.py
│   └── models.py
├── data/
│   └── users.json
│   └── pharmacies.json
├── init_db.py
├── create_db.py
├── phantom_mask.db
├── requirements.txt
└── response.md
```