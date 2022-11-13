# Argus
Log system for Zoho


## Documentation

Simple project to monitor custome functions of ZOHO Desk


## API Reference

#### Function entry point

```http
  POST /api/v1/log-in
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `function` | `string` | **Required**. Function name |
| `departmentId` | `int` | **Required**. Department ZOHO Id |
| `ticketId` | `int` | **Required**. Ticket ZOHO Id |

#### Get item

```http
  POST /api/v1/log-out
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `function` | `string` | **Required**. Function name |
| `departmentId` | `int` | **Required**. Department ZOHO Id |
| `ticketId` | `int` | **Required**. Ticket ZOHO Id |
| `key` | `int` | **Required**. Key from Argus |

