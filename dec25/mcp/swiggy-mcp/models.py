"""
This module has pydantic models
"""

from typing import Annotated, List, Optional
from datetime import datetime, date
from enum import Enum
from pydantic import BaseModel, Field


class Restaurant(BaseModel):
    """Represents a restaurant from which the order was placed.

    Attributes:
        restaurantId (str): Unique restaurant identifier.
        name (str): Restaurant name.
        location (str): Location or address of the restaurant.
        cuisine (str): Type of cuisine served (e.g., Indian, Chinese).
        rating (float): Rating between 0–5.
        deliveryTime (str): Estimated delivery time in minutes.
    """
    restaurantId: Annotated[str|None, Field(default=None,alias="restaurantId")] = None
    name: Annotated[str, Field()]
    location: Annotated[str, Field()]
    cuisine: Annotated[str | None, Field(default=None, description="Optional comment")] = None
    rating: Annotated[float, Field(ge=0, le=5)]
    deliveryTime: Annotated[str, Field()]


class OrderModel(BaseModel):
    """Basic order information including customer identity.

    Attributes:
        orderId (str): Unique order identifier (min length 5).
        customerId (str): Unique customer identifier.
        customerName (str): Name of the customer.
    """
    orderId: Annotated[str, Field(description="Order Id", min_length=5)]
    customerId: Annotated[str, Field(description="Customer Id", min_length=5)]
    customerName: Annotated[str, Field(description="Customer Name", min_length=5)]


class OrderStatus(str, Enum):
    """Enumerates supported order statuses."""
    delivered = "delivered"
    cancelled = "cancelled"
    pending = "pending"
    preparing = "preparing"
    out_for_delivery = "out_for_delivery"


class Item(BaseModel):
    """Represents an individual item in an order.

    Attributes:
        name (str): Item name.
        quantity (int): Number of units ordered; must be ≥1.
        price (float): Price of a single item.
        customizations (List[str]): Extra customization notes (e.g., 'extra cheese').
    """
    name: Annotated[str, Field()]
    quantity: Annotated[int, Field(ge=1)]
    price: Annotated[float, Field(ge=0)]
    customizations: Annotated[List[str], Field(default_factory=list)]


class Pricing(BaseModel):
    """Stores pricing breakdown for an order.

    Attributes:
        itemTotal (float): Cost of all items before fees.
        deliveryFee (float): Fee charged for delivery.
        platformFee (float): Platform/handling charges.
        gst (float): Applicable GST.
        discount (float): Discount applied.
        totalAmount (float): Final payable amount.
    """
    itemTotal: Annotated[float, Field(ge=0)]
    deliveryFee: Annotated[float, Field(ge=0)]
    platformFee: Annotated[float, Field(ge=0)]
    gst: Annotated[float, Field(ge=0)]
    discount: Annotated[float, Field(ge=0)]
    totalAmount: Annotated[float, Field(ge=0)]


class Payment(BaseModel):
    """Represents payment information for an order.

    Attributes:
        method (str): Payment method used.
        transactionId (str): Unique transaction reference.
        status (str): Payment status (e.g., successful, failed).
    """
    method: Annotated[str, Field()]
    transactionId: Annotated[str, Field(alias="transactionId")]
    status: Annotated[str, Field()]


class DeliveryAddress(BaseModel):
    """Represents the delivery address for an order.

    Attributes:
        label (str): Address label (e.g., Home, Office).
        address (str): Full delivery address.
        city (str): City name.
        pincode (str): 6-digit pincode.
    """
    label: Annotated[str, Field()]
    address: Annotated[str, Field()]
    city: Annotated[str, Field()]
    pincode: Annotated[str, Field(min_length=6, max_length=6)]


class DeliveryPartner(BaseModel):
    """Information about the person delivering the order.

    Attributes:
        name (str): Delivery partner’s name.
        rating (float): Rating between 0–5.
        phone (str): Contact number.
    """
    name: Annotated[str, Field()]
    rating: Annotated[float, Field(ge=0, le=5)]
    phone: Annotated[str, Field()]


class Timeline(BaseModel):
    """Order lifecycle timestamps.

    Attributes:
        orderPlaced (datetime): When customer placed the order.
        restaurantAccepted (datetime): When restaurant confirmed order.
        foodReady (datetime): When food preparation finished.
        outForDelivery (datetime): When order left for delivery.
        delivered (datetime): Final delivery timestamp.
    """
    orderPlaced: Annotated[datetime, Field(alias="orderPlaced")]
    restaurantAccepted: Annotated[datetime, Field(alias="restaurantAccepted")]
    foodReady: Annotated[datetime, Field(alias="foodReady")]
    outForDelivery: Annotated[datetime, Field(alias="outForDelivery")]
    delivered: Annotated[datetime, Field(alias="delivered")]


class Ratings(BaseModel):
    """Ratings provided by the customer.

    Attributes:
        food (int): Food rating 1–5.
        delivery (int): Delivery rating 1–5.
        review (str): Free-text review.
    """
    food: Annotated[int, Field(ge=1, le=5)]
    delivery: Annotated[int, Field(ge=1, le=5)]
    review: Annotated[str, Field()]


class Order(BaseModel):
    """Represents the full order structure including pricing, items, delivery, and ratings.

    Attributes:
        orderId (str): Unique order identifier.
        customerId (str): Customer ID.
        customerName (str): Customer name.
        orderDate (datetime): Timestamp of order placement.
        status (OrderStatus): Current order status.
        restaurant (Restaurant): Restaurant details.
        items (List[Item]): List of items ordered.
        pricing (Pricing): Price breakdown.
        payment (Payment): Payment details.
        deliveryAddress (DeliveryAddress): Delivery Address.
        deliveryPartner (DeliveryPartner): Assigned delivery agent.
        timeline (Timeline): Full order timeline.
        ratings (Ratings): Post-delivery ratings.
    """
    orderId: Annotated[str, Field(alias="orderId")]
    customerId: Annotated[str, Field(alias="customerId")]
    customerName: Annotated[str, Field(alias="customerName")]
    orderDate: Annotated[datetime, Field(alias="orderDate")]
    status: Annotated[OrderStatus, Field()]
    restaurant: Restaurant
    items: Annotated[List[Item], Field()]
    pricing: Pricing
    payment: Payment
    deliveryAddress: DeliveryAddress
    deliveryPartner: DeliveryPartner
    timeline: Timeline
    ratings: Ratings


class SpiceLevel(str, Enum):
    """Represents preferred spice levels for the customer."""
    Mild = "Mild"
    Medium = "Medium"
    Hot = "Hot"


class RecentOrder(BaseModel):
    """Represents a customer’s recent order history entry."""
    orderId: Annotated[str, Field(alias="orderId")]
    orderDate: Annotated[datetime, Field(alias="orderDate")]
    status: Annotated[OrderStatus, Field()]
    restaurant: Restaurant
    items: Annotated[List[Item], Field()]
    pricing: Pricing
    payment: Payment
    deliveryAddress: DeliveryAddress
    deliveryPartner: DeliveryPartner
    timeline: Timeline
    ratings: Ratings


class Profile(BaseModel):
    """Represents the user profile details.

    Attributes:
        name (str): Full name.
        email (str): Email address.
        phone (str): Phone number.
        memberSince (date): Date of joining.
    """
    name: Annotated[str, Field()]
    email: Annotated[str, Field()]
    phone: Annotated[str, Field()]
    memberSince: Annotated[date, Field(alias="memberSince")]


class AccountStats(BaseModel):
    """Lifetime statistics of the user’s account.

    Attributes:
        totalOrders (int): Total number of completed orders.
        lifetimeValue (float): Total money spent.
        averageOrderValue (float): Average price per order.
        favoriteRestaurants (List[str]): List of favorite restaurants.
        preferredCuisines (List[str]): Cuisines most frequently ordered.
        savedAddresses (int): Number of saved addresses.
    """
    totalOrders: Annotated[int, Field(ge=0)]
    lifetimeValue: Annotated[float, Field(ge=0)]
    averageOrderValue: Annotated[float, Field(ge=0)]
    favoriteRestaurants: Annotated[List[str], Field(default_factory=list)]
    preferredCuisines: Annotated[List[str], Field(default_factory=list)]
    savedAddresses: Annotated[int, Field(ge=0)]


class Preferences(BaseModel):
    """Customer-specific preferences for food ordering.

    Attributes:
        dietaryRestrictions (List[str]): Restrictions like Vegan, No sugar etc.
        favoriteItems (List[str]): Frequently ordered food items.
        avoidIngredients (List[str]): Ingredients customer avoids.
        spiceLevel (SpiceLevel): Preferred spice level.
    """
    dietaryRestrictions: Annotated[List[str], Field(default_factory=list)]
    favoriteItems: Annotated[List[str], Field(default_factory=list)]
    avoidIngredients: Annotated[List[str], Field(default_factory=list)]
    spiceLevel: Annotated[SpiceLevel, Field()]


class Coupon(BaseModel):
    """Represents an available coupon for the customer."""
    code: Annotated[str, Field()]
    description: Annotated[str, Field()]
    validUntil: Annotated[date, Field(alias="validUntil")]


class LoyaltyRewards(BaseModel):
    """Tracks the customer's loyalty reward points and coupons."""
    currentPoints: Annotated[int, Field(ge=0)]
    pointsToNextReward: Annotated[int, Field(ge=0)]
    couponsAvailable: Annotated[List[Coupon], Field(default_factory=list)]


class Customer(BaseModel):
    """Main customer model including profile, stats, preferences, and recent orders.

    Attributes:
        customerId (str): Unique customer ID.
        profile (Profile): Personal profile information.
        accountStats (AccountStats): Lifetime ordering analytics.
        recentOrders (List[RecentOrder]): Recent orders placed.
        preferences (Preferences): Customer food preferences.
        loyaltyRewards (LoyaltyRewards): Points & coupon information.
    """
    customerId: Annotated[str, Field(alias="customerId")]
    profile: Profile
    accountStats: AccountStats
    recentOrders: Annotated[List[RecentOrder], Field(default_factory=list)]
    preferences: Preferences
    loyaltyRewards: LoyaltyRewards
