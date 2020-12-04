//
//  Item.swift
//  Gai Gai
//
//  Created by Stephen Tang on 19/1/19.
//  Copyright © 2019 Stephen Tang. All rights reserved.
//

import Foundation
import UIKit

class Item {
    
    var name: String
    var description: String
    var category_name: String
    var provider: String
    var price: Double
    var image: UIImage
    var url: URL
    var rating: Double
    
    init(name: String, description: String, category_name: String, provider: String, price: Double, image: UIImage, url: URL, rating: Double) {
        
        self.name = name
        self.description = description
        self.category_name = category_name
        self.provider = provider
        self.price = price
        self.image = image
        self.url = url
        self.rating = rating
    }
}
